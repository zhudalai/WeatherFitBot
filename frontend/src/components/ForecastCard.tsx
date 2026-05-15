import React from 'react';
import type { ForecastDay } from '../types';
import type { Lang } from '../i18n';
import { t } from '../i18n';

interface ForecastCardProps {
  forecast: ForecastDay[];
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

const WEEKDAYS: Record<Lang, string[]> = {
  zh: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
  en: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
  ja: ['日', '月', '火', '水', '木', '金', '土'],
};

function formatDate(dateStr: string, lang: Lang): string {
  const date = new Date(dateStr);
  const dayName = WEEKDAYS[lang][date.getDay()];
  if (lang === 'zh') {
    return `${date.getMonth() + 1}/${date.getDate()} ${dayName}`;
  }
  if (lang === 'ja') {
    return `${date.getMonth() + 1}/${date.getDate()}（${dayName}）`;
  }
  return `${dayName} ${date.getMonth() + 1}/${date.getDate()}`;
}

const ForecastCard: React.FC<ForecastCardProps> = ({ forecast, lang = "zh" }) => {
  return (
    <div className="rounded-xl bg-gradient-to-br from-purple-50 to-pink-100 p-4 shadow-sm">
      <h4 className="mb-3 text-base font-semibold text-gray-800">📅 {t(lang, 'forecast')}</h4>
      <div className="grid grid-cols-5 gap-2">
        {forecast.map((day) => (
          <div
            key={day.date}
            className="flex flex-col items-center rounded-lg bg-white/60 p-2 text-center"
          >
            <span className="text-xs text-gray-500">{formatDate(day.date, lang)}</span>
            <span className="my-1 text-xl">{iconMap[day.icon] || '🌤️'}</span>
            <span className="text-xs text-gray-600">{day.description}</span>
            <span className="mt-1 text-sm font-medium text-gray-800">
              {day.temp_max.toFixed(0)}° / {day.temp_min.toFixed(0)}°
            </span>
            {day.rain_probability > 0.2 && (
              <span className="mt-1 text-xs text-blue-600">
                💧 {(day.rain_probability * 100).toFixed(0)}%
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ForecastCard;
