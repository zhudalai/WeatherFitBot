from pydantic import BaseModel
from typing import Optional


class CurrentWeather(BaseModel):
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_direction: int
    description: str
    icon: str
    visibility: int = 10000
    uv_index: Optional[float] = None
    rain_probability: float = 0.0


class ForecastDay(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    description: str
    icon: str
    humidity: int
    rain_probability: float = 0.0
    wind_speed: float = 0.0


class WeatherResponse(BaseModel):
    city: str
    country: str
    current: CurrentWeather
    forecast: list[ForecastDay]
