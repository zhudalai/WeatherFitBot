from fastapi import APIRouter, HTTPException
from app.services.weather_service import WeatherService
from app.services.city_resolver import CityResolver

router = APIRouter(prefix="/api/weather", tags=["weather"])
weather_service = WeatherService()


@router.get("/{city_name}")
async def get_weather(city_name: str):
    """获取城市天气"""
    city = CityResolver.resolve(city_name)
    if not city:
        raise HTTPException(status_code=400, detail="Invalid city name")

    try:
        result = await weather_service.get_weather(city)
        return {"code": 200, "message": "success", "data": result.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"City '{city_name}' not found: {str(e)}")
