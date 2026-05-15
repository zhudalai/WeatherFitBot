import { useState, useCallback, useRef } from 'react';
import { sendMessage, type ChatResult } from '../services/api';
import type { ChatMessage, WeatherData, QuickAction } from '../types';
import { t, type Lang } from '../i18n';

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

function getWelcomeMessage(lang: Lang): string {
  return t(lang, 'welcome');
}

function getQuickActions(lang: Lang): QuickAction[] {
  return [
    { label: t(lang, 'cityBeijing'), action: t(lang, 'cityBeijing').replace('📍 ', '') },
    { label: t(lang, 'cityShanghai'), action: t(lang, 'cityShanghai').replace('📍 ', '') },
    { label: t(lang, 'cityTokyo'), action: t(lang, 'cityTokyo').replace('📍 ', '') },
  ];
}

function getChangeCityActions(lang: Lang): QuickAction[] {
  return [
    { label: t(lang, 'cityBeijing'), action: t(lang, 'cityBeijing').replace('📍 ', '') },
    { label: t(lang, 'cityShanghai'), action: t(lang, 'cityShanghai').replace('📍 ', '') },
    { label: t(lang, 'cityLondon'), action: t(lang, 'cityLondon').replace('📍 ', '') },
    { label: t(lang, 'cityParis'), action: t(lang, 'cityParis').replace('📍 ', '') },
  ];
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const sessionIdRef = useRef<string | undefined>(undefined);
  const langRef = useRef<Lang>("zh");

  const addMessage = useCallback((msg: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    const newMsg: ChatMessage = {
      ...msg,
      id: generateId(),
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMsg]);
    return newMsg.id;
  }, []);

  const updateMessage = useCallback((id: string, updates: Partial<ChatMessage>) => {
    setMessages((prev) =>
      prev.map((msg) => (msg.id === id ? { ...msg, ...updates } : msg))
    );
  }, []);

  const initWelcome = useCallback((lang: Lang) => {
    langRef.current = lang;
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: getWelcomeMessage(lang),
        timestamp: new Date(),
        quickActions: getQuickActions(lang),
      },
    ]);
  }, []);

  const handleSend = useCallback(
    async (content: string) => {
      if (!content.trim() || isLoading) return;

      // 首次发送时初始化欢迎消息
      if (messages.length === 0) {
        initWelcome(langRef.current);
      }

      addMessage({ role: 'user', content: content.trim() });

      const loadingId = addMessage({
        role: 'assistant',
        content: '',
        isLoading: true,
      });

      setIsLoading(true);

      try {
        const result: ChatResult = await sendMessage(content, sessionIdRef.current);

        let weatherData: WeatherData | undefined;
        if (result.data) {
          weatherData = {
            city: result.data.city,
            country: result.data.country,
            current_weather: result.data.current_weather as unknown as WeatherData['current_weather'],
            outfit_advice: result.data.outfit_advice as unknown as WeatherData['outfit_advice'],
            forecast: result.data.forecast as unknown as WeatherData['forecast'],
          };
        }

        updateMessage(loadingId, {
          content: result.reply,
          data: weatherData,
          quickActions: result.quick_actions,
          isLoading: false,
        });
      } catch (error) {
        const errorMsg = error instanceof Error ? error.message : '未知错误';
        const lang = langRef.current;
        updateMessage(loadingId, {
          content: `${t(lang, 'requestFailed')}${errorMsg}${t(lang, 'checkBackend')}`,
          isLoading: false,
          quickActions: [{ label: t(lang, 'retry'), action: 'retry' }],
        });
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, messages.length, addMessage, updateMessage, initWelcome]
  );

  const handleQuickAction = useCallback(
    (action: string) => {
      const lang = langRef.current;

      if (action === 'retry') {
        const lastUserMsg = [...messages].reverse().find((m) => m.role === 'user');
        if (lastUserMsg) {
          handleSend(lastUserMsg.content);
        }
      } else if (action === 'change_city') {
        addMessage({
          role: 'assistant',
          content: t(lang, 'changeCityPrompt'),
          quickActions: getChangeCityActions(lang),
        });
      } else if (action === 'view_forecast') {
        addMessage({
          role: 'assistant',
          content: t(lang, 'viewForecastPrompt'),
        });
      } else {
        handleSend(action);
      }
    },
    [messages, handleSend, addMessage]
  );

  return {
    messages,
    isLoading,
    sendMessage: handleSend,
    handleQuickAction,
    initWelcome,
  };
}
