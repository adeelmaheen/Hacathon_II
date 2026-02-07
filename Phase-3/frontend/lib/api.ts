/** API client for backend communication */
import axios, { AxiosError } from 'axios';
import type { LoginRequest, SignupRequest, Task, User } from '@/types';
import { auth } from './auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to every request
api.interceptors.request.use((config) => {
  const token = auth.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors (unauthorized)
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Clear auth and redirect to login
      auth.clearAuth();
      if (typeof window !== 'undefined') {
        window.location.href = '/';
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  signup: async (data: SignupRequest) => {
    const response = await api.post<{ access_token: string; token_type: string; user: User }>('/api/auth/signup', data);
    return response.data;
  },

  login: async (data: LoginRequest) => {
    const response = await api.post<{ access_token: string; token_type: string; user: User }>('/api/auth/login', data);
    return response.data;
  },
};

// Task API
export const taskAPI = {
  list: async (userId: number): Promise<Task[]> => {
    const response = await api.get<Task[]>(`/api/${userId}/tasks`);
    return response.data;
  },

  create: async (userId: number, data: { title: string; description?: string }): Promise<Task> => {
    const response = await api.post<Task>(`/api/${userId}/tasks`, data);
    return response.data;
  },

  get: async (userId: number, taskId: number): Promise<Task> => {
    const response = await api.get<Task>(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },

  update: async (userId: number, taskId: number, data: Partial<Task>): Promise<Task> => {
    const response = await api.put<Task>(`/api/${userId}/tasks/${taskId}`, data);
    return response.data;
  },

  delete: async (userId: number, taskId: number): Promise<void> => {
    await api.delete(`/api/${userId}/tasks/${taskId}`);
  },

  toggleComplete: async (userId: number, taskId: number): Promise<Task> => {
    const response = await api.patch<Task>(`/api/${userId}/tasks/${taskId}/complete`);
    return response.data;
  },
};

// Chat API
export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: string[];
}

export const chatAPI = {
  sendMessage: async (userId: number, data: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>(`/api/${userId}/chat`, data);
    return response.data;
  },
};

