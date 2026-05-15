import React from 'react';
import type { CurrentWeather } from '../types';
import type { Lang } from '../i18n';
import { t } from '../i18n';

interface WeatherCardProps {
  weather: CurrentWeather;
  city: string;
  country: string;
  lang?: Lang;
}

const iconMap: Record<string, string> = {
  '01d': '☀️', '01n': '🌙',
  '02d': '⛅', '02n': '☁️',
  '03d': '☁️', '03n': '☁️',
  '04d': '☁️', '04n': '☁️',
  '09d': '🌧️', '09n': '🌧️',
  '10d': '🌦️', '10n': '🌧️',
  '11d': '⛈️', '11n': '⛈️',
  '13d': '❄️', '13n': '❄️',
  '50d': '🌫️', '50n': '🌫️',
};

const WeatherCard: React.FC<WeatherCardProps> = ({ weather, city, country, lang = "zh" }) => {
  const icon = iconMap[weather.icon] || '🌤️';

  return (
    <div className="rounded-xl bg-gradient-to-br from-blue-50 to-indigo-100 p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">
            {icon} {city}, {country}
          </h3>
          <p className="text-3xl font-bold text-gray-900">
            {weather.temperature.toFixed(0)}°C
          </p>
          <p className="text-sm text-gray-600">
            {t(lang, 'feelsLike')} {weather.feels_like.toFixed(0)}°C · {weather.description}
          </p>
        </div>
        <div className="text-right text-sm text-gray-600">
          <p>💧 {t(lang, 'humidity')} {weather.humidity}%</p>
          <p>💨 {t(lang, 'windSpeed')} {weather.wind_speed.toFixed(1)}m/s</p>
          <p>🌡️ {t(lang, 'tempRange').replace('{min}', weather.temp_min.toFixed(0)).replace('{max}', weather.temp_max.toFixed(0))}</p>
        </div>
      </div>
    </div>
  );
};

export default WeatherCard;
