/** TypeScript types for the application */

export interface User {
  id: number;
  email: string;
  name: string;
}

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  tags?: string[] | null;
  due_date?: string | null;
  reminder_time?: string | null;
  recurrence_pattern?: string | null;
  recurrence_interval?: number | null;
  next_due_date?: string | null;
  parent_task_id?: number | null;
  created_at: string;
  updated_at: string;
}

export type Priority = 'low' | 'medium' | 'high' | 'urgent';
export type RecurrencePattern = 'daily' | 'weekly' | 'monthly' | 'yearly' | 'custom';
export type SortBy = 'created_at' | 'due_date' | 'priority' | 'title';
export type SortOrder = 'asc' | 'desc';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

