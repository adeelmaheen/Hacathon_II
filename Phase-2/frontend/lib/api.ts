/**
 * Centralized API client for making requests to the backend.
 * Handles authentication headers and base URL configuration.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface ApiError {
  detail: string
}

export class ApiClient {
  private baseURL: string

  constructor(baseURL: string = API_URL) {
    this.baseURL = baseURL
  }

  /**
   * Make an authenticated API request.
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`

    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      credentials: 'include', // Include HTTPOnly cookies
    }

    const response = await fetch(url, config)

    // Handle non-2xx responses
    if (!response.ok) {
      const error: ApiError = await response.json().catch(() => ({
        detail: 'An unexpected error occurred',
      }))
      throw new Error(error.detail)
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T
    }

    return response.json()
  }

  /**
   * GET request
   */
  async get<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' })
  }

  /**
   * POST request
   */
  async post<T>(
    endpoint: string,
    data?: unknown,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  /**
   * PUT request
   */
  async put<T>(
    endpoint: string,
    data?: unknown,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  /**
   * PATCH request
   */
  async patch<T>(
    endpoint: string,
    data?: unknown,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  /**
   * DELETE request
   */
  async delete<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' })
  }
}

// Export singleton instance
export const apiClient = new ApiClient()

/**
 * Authentication API methods
 */
import { RegisterFormData, LoginFormData, TokenResponse, UserResponse } from "@/types/user";

export async function register(data: RegisterFormData): Promise<UserResponse> {
  return apiClient.post<UserResponse>("/api/auth/register", data);
}

export async function login(data: LoginFormData): Promise<TokenResponse> {
  return apiClient.post<TokenResponse>("/api/auth/login", data);
}

export async function logout(): Promise<{ message: string }> {
  return apiClient.post<{ message: string }>("/api/auth/logout");
}

/**
 * Task API methods
 */
import { Task, TaskCreate, TaskUpdate, TaskResponse, TaskFilters } from "@/types/task";

export async function getTasks(filters?: Partial<TaskFilters>): Promise<Task[]> {
  const params = new URLSearchParams();

  if (filters?.status && filters.status !== 'all') {
    params.append('status', filters.status);
  }
  if (filters?.sort) {
    params.append('sort', filters.sort);
  }
  if (filters?.order) {
    params.append('order', filters.order);
  }

  const query = params.toString();
  const endpoint = query ? `/api/tasks?${query}` : '/api/tasks';

  return apiClient.get<Task[]>(endpoint);
}

export async function createTask(data: TaskCreate): Promise<TaskResponse> {
  return apiClient.post<TaskResponse>("/api/tasks", data);
}

export async function updateTask(taskId: number, data: TaskUpdate): Promise<TaskResponse> {
  return apiClient.put<TaskResponse>(`/api/tasks/${taskId}`, data);
}

export async function toggleTask(taskId: number): Promise<TaskResponse> {
  return apiClient.patch<TaskResponse>(`/api/tasks/${taskId}/toggle`);
}

export async function deleteTask(taskId: number): Promise<void> {
  return apiClient.delete<void>(`/api/tasks/${taskId}`);
}
