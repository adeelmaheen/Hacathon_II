/**
 * Registration form component with validation and error handling.
 *
 * Features:
 * - Zod schema validation
 * - Real-time error display
 * - Email format validation
 * - Password strength requirements
 * - Accessible form inputs
 */
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { registerSchema, RegisterFormData } from "@/lib/validators";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export function RegisterForm() {
  const router = useRouter();
  const { register, loading, error: authError } = useAuth();

  const [formData, setFormData] = useState<RegisterFormData>({
    email: "",
    name: "",
    password: "",
  });

  const [errors, setErrors] = useState<Partial<Record<keyof RegisterFormData, string>>>({});

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
    if (errors[name as keyof RegisterFormData]) {
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
    const result = registerSchema.safeParse(formData);

    if (!result.success) {
      // Extract field errors from Zod
      const fieldErrors: Partial<Record<keyof RegisterFormData, string>> = {};
      result.error.errors.forEach((err) => {
        const field = err.path[0] as keyof RegisterFormData;
        fieldErrors[field] = err.message;
      });
      setErrors(fieldErrors);
      return;
    }

    try {
      await register(result.data);
      // AuthContext will handle redirect to dashboard
    } catch (err) {
      // Error handled by AuthContext
      console.error("Registration error:", err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Global error from API */}
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

      {/* Name field */}
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
          Name
        </label>
        <Input
          id="name"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
          error={errors.name}
          placeholder="John Doe"
          autoComplete="name"
          required
        />
        {errors.name && (
          <p className="mt-1 text-sm text-red-600" role="alert">
            {errors.name}
          </p>
        )}
      </div>

      {/* Password field */}
      <div>
        <Input
          id="password"
          name="password"
          type="password"
          label="Password"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          placeholder="At least 8 characters"
          helperText="Password must be at least 8 characters long"
          autoComplete="new-password"
          showPasswordToggle
          required
        />
      </div>

      {/* Submit button */}
      <Button
        type="submit"
        variant="primary"
        className="w-full"
        disabled={loading}
        aria-label="Create account"
      >
        {loading ? "Creating account..." : "Create Account"}
      </Button>

      {/* Link to login */}
      <p className="text-center text-sm text-gray-600">
        Already have an account?{" "}
        <a
          href="/login"
          className="font-medium text-blue-600 hover:text-blue-500 underline"
        >
          Log in
        </a>
      </p>
    </form>
  );
}
