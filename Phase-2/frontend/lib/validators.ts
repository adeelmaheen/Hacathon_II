/**
 * Zod validation schemas for form validation.
 *
 * These schemas provide client-side validation matching the backend
 * Pydantic schemas to ensure consistent validation rules.
 */
import { z } from "zod";

/**
 * Registration form validation schema.
 *
 * Validates:
 * - Email format (standard email regex)
 * - Name (1-100 characters, not whitespace only)
 * - Password (8-72 characters minimum, bcrypt limit)
 */
export const registerSchema = z.object({
  email: z
    .string()
    .min(1, "Email is required")
    .email("Invalid email format")
    .toLowerCase()
    .transform((val) => val.trim()),

  name: z
    .string()
    .min(1, "Name is required")
    .max(100, "Name must be 100 characters or less")
    .refine((val) => val.trim().length > 0, {
      message: "Name cannot be whitespace only",
    })
    .transform((val) => val.trim()),

  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(72, "Password must be 72 characters or less"),
});

/**
 * Login form validation schema.
 *
 * Validates:
 * - Email format
 * - Password presence (no length check on login for security)
 */
export const loginSchema = z.object({
  email: z
    .string()
    .min(1, "Email is required")
    .email("Invalid email format")
    .toLowerCase()
    .transform((val) => val.trim()),

  password: z.string().min(1, "Password is required"),
});

/**
 * Task creation validation schema.
 *
 * Validates:
 * - Title (1-200 characters, not whitespace only)
 * - Description (optional, max 1000 characters)
 */
export const taskCreateSchema = z.object({
  title: z
    .string()
    .min(1, "Title is required")
    .max(200, "Title must be 200 characters or less")
    .refine((val) => val.trim().length > 0, {
      message: "Title cannot be whitespace only",
    })
    .transform((val) => val.trim()),

  description: z
    .string()
    .max(1000, "Description must be 1000 characters or less")
    .optional()
    .transform((val) => {
      if (!val) return undefined;
      const trimmed = val.trim();
      return trimmed.length > 0 ? trimmed : undefined;
    }),
});

/**
 * Type inference from Zod schemas
 */
export type RegisterFormData = z.infer<typeof registerSchema>;
export type LoginFormData = z.infer<typeof loginSchema>;
export type TaskCreateFormData = z.infer<typeof taskCreateSchema>;
