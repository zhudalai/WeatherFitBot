import httpx
from app.config import settings
from app.cache.redis_client import cache
from app.models.weather import CurrentWeather, ForecastDay, WeatherResponse
from app.services.lang_detect import OWM_LANG_MAP


class WeatherService:
    """天气数据服务"""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    async def get_weather(self, city: str, lang: str = "zh") -> WeatherResponse:
        """获取城市天气（当前+预报）"""
        owm_lang = OWM_LANG_MAP.get(lang, "en")

        # 先查缓存（缓存 key 包含语言）
        cache_key = f"weather:{city.lower()}:{lang}"
        cached = await cache.get_json(cache_key)
        if cached:
            return WeatherResponse(**cached)

        # 调用 API
        async with httpx.AsyncClient() as client:
            # 当前天气
            current_resp = await client.get(
                f"{self.BASE_URL}/weather",
                params={
                    "q": city,
                    "appid": settings.openweather_api_key,
                    "units": "metric",
                    "lang": owm_lang,
                },
                timeout=10.0,
            )
            current_resp.raise_for_status()
            current_data = current_resp.json()

            # 5天预报
            forecast_resp = await client.get(
                f"{self.BASE_URL}/forecast",
                params={
                    "q": city,
                    "appid": settings.openweather_api_key,
                    "units": "metric",
                    "lang": owm_lang,
                },
                timeout=10.0,
            )
            forecast_resp.raise_for_status()
            forecast_data = forecast_resp.json()

        # 解析当前天气
        current = CurrentWeather(
            temperature=current_data["main"]["temp"],
            feels_like=current_data["main"]["feels_like"],
            temp_min=current_data["main"]["temp_min"],
            temp_max=current_data["main"]["temp_max"],
            humidity=current_data["main"]["humidity"],
            pressure=current_data["main"]["pressure"],
            wind_speed=current_data["wind"]["speed"],
            wind_direction=current_data["wind"].get("deg", 0),
            description=current_data["weather"][0]["description"],
            icon=current_data["weather"][0]["icon"],
            visibility=current_data.get("visibility", 10000),
            rain_probability=current_data.get("pop", 0),
        )

        # 解析预报
        forecast = self._parse_forecast(forecast_data)

        result = WeatherResponse(
            city=current_data["name"],
            country=current_data["sys"]["country"],
            current=current,
            forecast=forecast,
        )

        # 写入缓存
        await cache.set_json(cache_key, result.model_dump(), settings.weather_cache_ttl)

        return result

    def _parse_forecast(self, data: dict) -> list[ForecastDay]:
        """解析 5 天预报数据，每天取一个代表"""
        daily: dict = {}
        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]
            if date not in daily:
                daily[date] = {
                    "temps": [],
                    "descriptions": [],
                    "icons": [],
                    "humidity": [],
                    "wind": [],
                    "pop": [],
                }
            daily[date]["temps"].append(item["main"]["temp"])
            daily[date]["descriptions"].append(item["weather"][0]["description"])
            daily[date]["icons"].append(item["weather"][0]["icon"])
            daily[date]["humidity"].append(item["main"]["humidity"])
            daily[date]["wind"].append(item["wind"]["speed"])
            daily[date]["pop"].append(item.get("pop", 0))

        forecast = []
        for date, vals in list(daily.items())[:5]:
            desc = max(set(vals["descriptions"]), key=vals["descriptions"].count)
            icon = max(set(vals["icons"]), key=vals["icons"].count)
            forecast.append(
                ForecastDay(
                    date=date,
                    temp_max=max(vals["temps"]),
                    temp_min=min(vals["temps"]),
                    description=desc,
                    icon=icon,
                    humidity=int(sum(vals["humidity"]) / len(vals["humidity"])),
                    rain_probability=max(vals["pop"]),
                    wind_speed=max(vals["wind"]),
                )
            )

        return forecast
