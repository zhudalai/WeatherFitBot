import uuid
from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse, QuickAction
from app.services.weather_service import WeatherService
from app.services.outfit_service import OutfitService
from app.services.city_resolver import CityResolver
from app.services.lang_detect import detect_language, resolve_ja_city

router = APIRouter(prefix="/api/chat", tags=["chat"])
weather_service = WeatherService()
outfit_service = OutfitService()

# 快捷按钮多语言
QA_LABELS = {
    "zh": {"change_city": "换个城市", "view_forecast": "查看未来几天", "retry": "重试"},
    "en": {"change_city": "Change city", "view_forecast": "View forecast", "retry": "Retry"},
    "ja": {"change_city": "都市を変更", "view_forecast": "天気予報を見る", "retry": "再試行"},
}

# 错误回复多语言
ERROR_REPLIES = {
    "zh": "抱歉，无法获取 '{city}' 的天气信息。请检查城市名称是否正确，或稍后再试。\n\n错误：{error}",
    "en": "Sorry, couldn't get weather for '{city}'. Please check the city name and try again.\n\nError: {error}",
    "ja": "申し訳ありません。「{city}」の天気情報を取得できませんでした。都市名を確認して再度お試しください。\n\nエラー：{error}",
}


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天接口"""
    session_id = request.session_id or str(uuid.uuid4())
    user_message = request.message.strip()

    # 检测用户语言
    lang = detect_language(user_message)

    # 解析城市名
    city = CityResolver.resolve(user_message)
    if not city:
        city = user_message

    # 日语城市名 → 转为英文查询名（OpenWeatherMap 不支持日文城市名）
    if lang == "ja":
        city = resolve_ja_city(city)

    labels = QA_LABELS.get(lang, QA_LABELS["zh"])

    try:
        # 获取天气（传入语言）
        weather = await weather_service.get_weather(city, lang)

        # 生成穿搭建议（传入语言）
        outfit = await outfit_service.generate_outfit(weather, lang)

        # 构建回复（根据语言选择模板）
        reply = _build_reply(weather, outfit, lang)

        data = {
            "city": weather.city,
            "country": weather.country,
            "current_weather": weather.current.model_dump(),
            "outfit_advice": outfit.model_dump(),
            "forecast": [f.model_dump() for f in weather.forecast],
        }

        quick_actions = [
            QuickAction(label=labels["change_city"], action="change_city"),
            QuickAction(label=labels["view_forecast"], action="view_forecast"),
        ]

        return ChatResponse(reply=reply, data=data, quick_actions=quick_actions)

    except Exception as e:
        reply = ERROR_REPLIES.get(lang, ERROR_REPLIES["en"]).format(
            city=user_message, error=str(e)
        )
        return ChatResponse(
            reply=reply,
            data=None,
            quick_actions=[QuickAction(label=labels["retry"], action="retry")],
        )


def _build_reply(weather, outfit, lang: str) -> str:
    """根据语言构建回复文本"""
    cw = weather.current
    if lang == "ja":
        return (
            f"📍 {weather.city}, {weather.country}\n"
            f"🌡️ 現在 {cw.temperature:.0f}°C"
            f"（体感 {cw.feels_like:.0f}°C）、{cw.description}\n"
            f"💧 湿度 {cw.humidity}%、"
            f"💨 風速 {cw.wind_speed:.1f}m/s\n\n"
            f"👔 コーディネート：{outfit.summary}\n"
            f"  上：{outfit.top}\n"
            f"  下：{outfit.bottom}\n"
            f"  靴：{outfit.shoes}\n"
            f"  小物：{outfit.accessories}\n"
            f"  💡 {outfit.tips}"
        )
    elif lang == "en":
        return (
            f"📍 {weather.city}, {weather.country}\n"
            f"🌡️ Currently {cw.temperature:.0f}°C"
            f" (feels like {cw.feels_like:.0f}°C), {cw.description}\n"
            f"💧 Humidity {cw.humidity}%, "
            f"💨 Wind {cw.wind_speed:.1f}m/s\n\n"
            f"👔 Outfit advice: {outfit.summary}\n"
            f"  Top: {outfit.top}\n"
            f"  Bottom: {outfit.bottom}\n"
            f"  Shoes: {outfit.shoes}\n"
            f"  Accessories: {outfit.accessories}\n"
            f"  💡 {outfit.tips}"
        )
    else:  # zh
        return (
            f"📍 {weather.city}, {weather.country}\n"
            f"🌡️ 当前 {cw.temperature:.0f}°C"
            f"（体感 {cw.feels_like:.0f}°C），{cw.description}\n"
            f"💧 湿度 {cw.humidity}%，"
            f"💨 风速 {cw.wind_speed:.1f}m/s\n\n"
            f"👔 穿搭建议：{outfit.summary}\n"
            f"  上装：{outfit.top}\n"
            f"  下装：{outfit.bottom}\n"
            f"  鞋履：{outfit.shoes}\n"
            f"  配件：{outfit.accessories}\n"
            f"  💡 {outfit.tips}"
        )
