import React from 'react';
import type { ChatMessage } from '../types';
import type { Lang } from '../i18n';
import WeatherCard from './WeatherCard';
import OutfitCard from './OutfitCard';
import ForecastCard from './ForecastCard';

interface MessageBubbleProps {
  message: ChatMessage;
  onQuickAction: (action: string) => void;
  lang: Lang;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onQuickAction, lang }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`message-enter flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[85%] md:max-w-[70%] ${
          isUser
            ? 'rounded-2xl rounded-br-md bg-blue-600 text-white'
            : 'rounded-2xl rounded-bl-md bg-white text-gray-800 shadow-md'
        } px-4 py-3`}
      >
        {message.isLoading ? (
          <div className="flex items-center gap-1 py-1">
            <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '0ms' }} />
            <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '150ms' }} />
            <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '300ms' }} />
          </div>
        ) : (
          <>
            <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>

            {/* 天气卡片 */}
            {message.data && (
              <div className="mt-3 space-y-3">
                <WeatherCard
                  weather={message.data.current_weather}
                  city={message.data.city}
                  country={message.data.country}
                  lang={lang}
                />
                <OutfitCard advice={message.data.outfit_advice} lang={lang} />
                {message.data.forecast && message.data.forecast.length > 0 && (
                  <ForecastCard forecast={message.data.forecast} lang={lang} />
                )}
              </div>
            )}

            {/* 快捷操作 */}
            {message.quickActions && message.quickActions.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2">
                {message.quickActions.map((qa) => (
                  <button
                    key={qa.action}
                    onClick={() => onQuickAction(qa.action)}
                    className="rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-xs text-gray-700 transition-colors hover:bg-gray-100"
                  >
                    {qa.label}
                  </button>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
