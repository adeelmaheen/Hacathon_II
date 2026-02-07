/**
 * User type definitions matching backend UserResponse schema.
 */

export interface User {
  id: string // UUID
  email: string
  name: string
  created_at: string // ISO 8601 date-time
}

export interface RegisterRequest {
  email: string
  name: string
  password: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface UserResponse extends User {}

export interface RegisterFormData {
  email: string
  name: string
  password: string
}

export interface LoginFormData {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: UserResponse
}
