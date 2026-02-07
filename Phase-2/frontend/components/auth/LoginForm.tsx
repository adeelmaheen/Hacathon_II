/**
 * Login form component with validation and error handling.
 *
 * Features:
 * - Zod schema validation
 * - Real-time error display
 * - Generic error messages for security
 * - Accessible form inputs
 */
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { loginSchema, LoginFormData } from "@/lib/validators";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export function LoginForm() {
  const router = useRouter();
  const { login, loading, error: authError } = useAuth();

  const [formData, setFormData] = useState<LoginFormData>({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState<Partial<Record<keyof LoginFormData, string>>>({});

  /**
   * Handle input change with validation
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear field error when user starts typing
    if (errors[name as keyof LoginFormData]) {
      setErrors((prev) => ({
        ...prev,
        [name]: undefined,
      }));
    }
  };

  /**
   * Handle form submission
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate with Zod
    const result = loginSchema.safeParse(formData);

    if (!result.success) {
      // Extract field errors from Zod
      const fieldErrors: Partial<Record<keyof LoginFormData, string>> = {};
      result.error.errors.forEach((err) => {
        const field = err.path[0] as keyof LoginFormData;
        fieldErrors[field] = err.message;
      });
      setErrors(fieldErrors);
      return;
    }

    try {
      await login(result.data);
      // AuthContext will handle redirect to dashboard
    } catch (err) {
      // Error handled by AuthContext
      console.error("Login error:", err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Global error from API - generic message for security */}
      {authError && (
        <div
          className="p-4 text-sm text-red-800 bg-red-100 border border-red-200 rounded-lg"
          role="alert"
        >
          {authError}
        </div>
      )}

      {/* Email field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <Input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          placeholder="user@example.com"
          autoComplete="email"
          required
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600" role="alert">
            {errors.email}
          </p>
        )}
      </div>

      {/* Password field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <Input
          id="password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          placeholder="Enter your password"
          autoComplete="current-password"
          required
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600" role="alert">
            {errors.password}
          </p>
        )}
      </div>

      {/* Submit button */}
      <Button
        type="submit"
        variant="primary"
        className="w-full"
        disabled={loading}
        aria-label="Log in"
      >
        {loading ? "Logging in..." : "Log In"}
      </Button>

      {/* Link to register */}
      <p className="text-center text-sm text-gray-600">
        Don't have an account?{" "}
        <a
          href="/register"
          className="font-medium text-blue-600 hover:text-blue-500 underline"
        >
          Create account
        </a>
      </p>
    </form>
  );
}
