export interface CurrentWeather {
  temperature: number;
  feels_like: number;
  temp_min: number;
  temp_max: number;
  humidity: number;
  pressure: number;
  wind_speed: number;
  wind_direction: number;
  description: string;
  icon: string;
  visibility: number;
  uv_index?: number;
  rain_probability: number;
}

export interface ForecastDay {
  date: string;
  temp_max: number;
  temp_min: number;
  description: string;
  icon: string;
  humidity: number;
  rain_probability: number;
  wind_speed: number;
}

export interface OutfitAdvice {
  summary: string;
  top: string;
  bottom: string;
  shoes: string;
  accessories: string;
  tips: string;
}

export interface WeatherData {
  city: string;
  country: string;
  current_weather: CurrentWeather;
  outfit_advice: OutfitAdvice;
  forecast: ForecastDay[];
}

export interface QuickAction {
  label: string;
  action: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  data?: WeatherData;
  quickActions?: QuickAction[];
  isLoading?: boolean;
}
