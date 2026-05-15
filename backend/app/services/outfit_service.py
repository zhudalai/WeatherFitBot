import json
import httpx
from app.config import settings
from app.cache.redis_client import cache
from app.models.weather import WeatherResponse
from app.models.outfit import OutfitAdvice
from app.utils.prompts import OUTFIT_PROMPT_TEMPLATE
from app.services.lang_detect import PROMPT_LANG_MAP

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# 规则引擎多语言兜底
RULE_OUTFIT = {
    "zh": {
        "cold": {
            "top": "羽绒服或厚棉服", "bottom": "加厚长裤", "shoes": "保暖靴",
            "accessories": "围巾、手套、帽子", "tips": "气温很低，注意防寒保暖",
        },
        "cool": {
            "top": "毛衣或夹克外套", "bottom": "长裤", "shoes": "运动鞋或休闲鞋",
            "accessories": "薄围巾", "tips": "气温偏凉，注意保暖",
        },
        "mild": {
            "top": "长袖T恤或衬衫", "bottom": "长裤或九分裤", "shoes": "运动鞋或休闲鞋",
            "accessories": "太阳镜", "tips": "气温舒适，适合户外活动",
        },
        "hot": {
            "top": "短袖T恤或背心", "bottom": "短裤或薄款长裤", "shoes": "凉鞋或透气运动鞋",
            "accessories": "太阳镜、防晒霜", "tips": "气温较高，注意防晒补水",
        },
        "rain_accessories": "雨伞或雨衣",
        "rain_tips": "，有雨请带雨具",
        "summary": "今天{city}{desc}，{temp:.0f}°C，{tips}。",
    },
    "en": {
        "cold": {
            "top": "Down jacket or heavy coat", "bottom": "Thick pants", "shoes": "Warm boots",
            "accessories": "Scarf, gloves, hat", "tips": "Very cold, dress warmly",
        },
        "cool": {
            "top": "Sweater or jacket", "bottom": "Long pants", "shoes": "Sneakers or casual shoes",
            "accessories": "Light scarf", "tips": "Cool weather, keep warm",
        },
        "mild": {
            "top": "Long-sleeve T-shirt or shirt", "bottom": "Pants or cropped pants",
            "shoes": "Sneakers or casual shoes", "accessories": "Sunglasses",
            "tips": "Comfortable temperature, great for outdoor activities",
        },
        "hot": {
            "top": "Short-sleeve T-shirt or tank top", "bottom": "Shorts or light pants",
            "shoes": "Sandals or breathable sneakers", "accessories": "Sunscreen, sunglasses",
            "tips": "Hot, stay hydrated and use sun protection",
        },
        "rain_accessories": "Umbrella or raincoat",
        "rain_tips": ", bring rain gear",
        "summary": "Today in {city}: {desc}, {temp:.0f}°C. {tips}.",
    },
    "ja": {
        "cold": {
            "top": "ダウンジャケットや厚手のコート", "bottom": "厚手の長ズボン",
            "shoes": "防寒ブーツ", "accessories": "マフラー、手袋、帽子",
            "tips": "とても寒いので、しっかり防寒してください",
        },
        "cool": {
            "top": "セーターやジャケット", "bottom": "長ズボン",
            "shoes": "スニーカーカジュアルシューズ", "accessories": "薄手のマフラー",
            "tips": "少し涼しいので、暖かくしましょう",
        },
        "mild": {
            "top": "長袖Tシャツやシャツ", "bottom": "ズボンやクロップドパンツ",
            "shoes": "スニーカーカジュアルシューズ", "accessories": "サングラス",
            "tips": "過ごしやすい気温で、屋外活動に最適です",
        },
        "hot": {
            "top": "半袖Tシャツやタンクトップ", "bottom": "ショートパンツや薄手のズボン",
            "shoes": "サンダルや通気性のあるスニーカー",
            "accessories": "日焼け止め、サングラス",
            "tips": "暑いので、水分補給と日焼け対策を",
        },
        "rain_accessories": "傘やレインコート",
        "rain_tips": "、雨の場合は雨具をお持ちください",
        "summary": "今日の{city}：{desc}、{temp:.0f}°C。{tips}。",
    },
}


class OutfitService:
    """AI 穿搭建议服务（通过 OpenRouter 调用）"""

    async def generate_outfit(self, weather: WeatherResponse, lang: str = "zh") -> OutfitAdvice:
        """根据天气生成穿搭建议"""
        # 先查缓存
        cache_key = f"outfit:{weather.city.lower()}:{weather.current.temperature:.0f}:{lang}"
        cached = await cache.get_json(cache_key)
        if cached:
            return OutfitAdvice(**cached)

        # 构建 Prompt
        uv_line = f"\n- 紫外线指数：{weather.current.uv_index}" if weather.current.uv_index else ""
        prompt_lang = PROMPT_LANG_MAP.get(lang, "中文")
        prompt = OUTFIT_PROMPT_TEMPLATE.format(
            city=weather.city,
            temperature=weather.current.temperature,
            feels_like=weather.current.feels_like,
            description=weather.current.description,
            humidity=weather.current.humidity,
            wind_speed=weather.current.wind_speed,
            uv_line=uv_line,
            language=prompt_lang,
        )

        # 调用 OpenRouter
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    OPENROUTER_URL,
                    headers={
                        "Authorization": f"Bearer {settings.openrouter_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.openrouter_model,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 500,
                    },
                    timeout=30.0,
                )
                resp.raise_for_status()
                data = resp.json()
                content = data["choices"][0]["message"]["content"].strip()
                advice_data = json.loads(content)
                advice = OutfitAdvice(**advice_data)
        except Exception:
            advice = self._rule_based_outfit(weather, lang)

        # 写入缓存
        await cache.set_json(cache_key, advice.model_dump(), settings.forecast_cache_ttl)

        return advice

    def _rule_based_outfit(self, weather: WeatherResponse, lang: str = "zh") -> OutfitAdvice:
        """规则引擎兜底（多语言）"""
        r = RULE_OUTFIT.get(lang, RULE_OUTFIT["zh"])
        temp = weather.current.temperature
        desc = weather.current.description

        if temp < 5:
            level = "cold"
        elif temp < 15:
            level = "cool"
        elif temp < 25:
            level = "mild"
        else:
            level = "hot"

        outfit = r[level]
        accessories = outfit["accessories"]
        tips = outfit["tips"]

        # 雨天处理
        rain_keywords = {
            "zh": ["雨"],
            "en": ["rain", "drizzle", "shower"],
            "ja": ["雨", "霧雨"],
        }
        for kw in rain_keywords.get(lang, rain_keywords["en"]):
            if kw.lower() in desc.lower():
                accessories = r["rain_accessories"]
                tips += r["rain_tips"]
                break

        summary = r["summary"].format(
            city=weather.city, desc=desc, temp=temp, tips=tips
        )

        return OutfitAdvice(
            summary=summary,
            top=outfit["top"],
            bottom=outfit["bottom"],
            shoes=outfit["shoes"],
            accessories=accessories,
            tips=tips,
        )
