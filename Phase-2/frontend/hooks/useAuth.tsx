/**
 * Authentication context and hook for managing user authentication state.
 *
 * Provides:
 * - User authentication state
 * - Login, logout, and register methods
 * - Loading and error states
 */
"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { User, RegisterFormData, LoginFormData } from "@/types/user";
import * as api from "@/lib/api";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (data: LoginFormData) => Promise<void>;
  register: (data: RegisterFormData) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  /**
   * Initialize auth state from localStorage on mount
   */
  useEffect(() => {
    const initAuth = () => {
      try {
        const storedUser = localStorage.getItem("user");
        const storedToken = localStorage.getItem("access_token");

        if (storedUser && storedToken) {
          setUser(JSON.parse(storedUser));
        }
      } catch (err) {
        console.error("Error loading auth state:", err);
        // Clear invalid data
        localStorage.removeItem("user");
        localStorage.removeItem("access_token");
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  /**
   * Register a new user account
   */
  const register = async (data: RegisterFormData) => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.register(data);

      // After registration, automatically log in
      await login({ email: data.email, password: data.password });
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.detail || "Registration failed. Please try again.";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Login with email and password
   */
  const login = async (data: LoginFormData) => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.login(data);

      // Store token and user in localStorage
      localStorage.setItem("access_token", response.access_token);
      localStorage.setItem("user", JSON.stringify(response.user));

      setUser(response.user);

      // Redirect to dashboard after successful login
      router.push("/dashboard");
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.detail || "Login failed. Please check your credentials.";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Logout current user
   */
  const logout = async () => {
    try {
      setLoading(true);
      setError(null);

      await api.logout();

      // Clear localStorage
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");

      setUser(null);

      // Redirect to login page
      router.push("/login");
    } catch (err: any) {
      console.error("Logout error:", err);
      // Even if API call fails, clear local state
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      setUser(null);
      router.push("/login");
    } finally {
      setLoading(false);
    }
  };

  /**
   * Clear error message
   */
  const clearError = () => {
    setError(null);
  };

  const value: AuthContextType = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to access authentication context
 */
export function useAuth() {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
