import React, { useRef, useEffect } from 'react';
import { t, type Lang } from '../i18n';

interface InputBarProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  lang?: Lang;
}

const InputBar: React.FC<InputBarProps> = ({ onSend, disabled, lang = "zh" }) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const input = inputRef.current;
    if (input && input.value.trim() && !disabled) {
      onSend(input.value);
      input.value = '';
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        ref={inputRef}
        type="text"
        placeholder={t(lang, 'inputPlaceholder')}
        disabled={disabled}
        className="flex-1 rounded-full border border-gray-200 bg-white px-4 py-3 text-sm text-gray-800 shadow-sm outline-none transition-all placeholder:text-gray-400 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 disabled:bg-gray-100"
      />
      <button
        type="submit"
        disabled={disabled}
        className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-600 text-white shadow-sm transition-all hover:bg-blue-700 disabled:bg-gray-300 disabled:shadow-none"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="h-5 w-5"
        >
          <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
        </svg>
      </button>
    </form>
  );
};

export default InputBar;
