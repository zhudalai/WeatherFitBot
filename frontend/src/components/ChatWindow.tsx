import React, { useEffect, useRef } from 'react';
import type { ChatMessage } from '../types';
import type { Lang } from '../i18n';
import MessageBubble from './MessageBubble';

interface ChatWindowProps {
  messages: ChatMessage[];
  onQuickAction: (action: string) => void;
  lang: Lang;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages, onQuickAction, lang }) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6">
      <div className="mx-auto max-w-2xl">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} onQuickAction={onQuickAction} lang={lang} />
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};

export default ChatWindow;
