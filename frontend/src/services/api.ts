import axios from 'axios';
import type { QuickAction } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 30000,
});

export interface ChatResponseData {
  city: string;
  country: string;
  current_weather: Record<string, unknown>;
  outfit_advice: Record<string, unknown>;
  forecast: Record<string, unknown>[];
}

export interface ChatResult {
  reply: string;
  data?: ChatResponseData;
  quick_actions: QuickAction[];
}

export async function sendMessage(
  message: string,
  sessionId?: string
): Promise<ChatResult> {
  const response = await api.post('/api/chat', {
    message,
    session_id: sessionId,
  });
  return response.data;
}
