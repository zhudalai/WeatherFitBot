import React, { useState, useEffect, useRef } from 'react';
import ChatWindow from './components/ChatWindow';
import InputBar from './components/InputBar';
import { useChat } from './hooks/useChat';
import { LANG_OPTIONS, type Lang } from './i18n';

const App: React.FC = () => {
  const { messages, isLoading, sendMessage, handleQuickAction, initWelcome } = useChat();
  const [lang, setLang] = useState<Lang>("zh");
  const initialized = useRef(false);

  // 初始化欢迎消息
  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true;
      initWelcome(lang);
    }
  }, [initWelcome, lang]);

  // 语言切换时重新初始化欢迎消息
  const handleLangChange = () => {
    const currentIndex = LANG_OPTIONS.findIndex((o) => o.value === lang);
    const nextIndex = (currentIndex + 1) % LANG_OPTIONS.length;
    const nextLang = LANG_OPTIONS[nextIndex].value;
    setLang(nextLang);
    initWelcome(nextLang);
  };

  return (
    <div className="flex h-screen flex-col">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-white/20 bg-white/10 px-4 py-3 backdrop-blur-sm">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🌤️</span>
          <h1 className="text-lg font-bold text-white">WeatherFit</h1>
          <span className="rounded-full bg-white/20 px-2 py-0.5 text-xs text-white/80">
            {lang === "zh" ? "天气穿搭助手" : lang === "en" ? "Weather & Outfit" : "天気＆コーディネート"}
          </span>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleLangChange}
            className="rounded-full bg-white/20 px-3 py-1 text-xs text-white transition-colors hover:bg-white/30"
          >
            {LANG_OPTIONS.find((o) => o.value === lang)?.label} ▾
          </button>
          <div className="text-xs text-white/60">v0.1.0</div>
        </div>
      </header>

      {/* Chat Area */}
      <ChatWindow messages={messages} onQuickAction={handleQuickAction} lang={lang} />

      {/* Input Area */}
      <div className="border-t border-white/10 bg-white/5 px-4 py-3 backdrop-blur-sm">
        <div className="mx-auto max-w-2xl">
          <InputBar onSend={sendMessage} disabled={isLoading} lang={lang} />
        </div>
      </div>
    </div>
  );
};

export default App;
