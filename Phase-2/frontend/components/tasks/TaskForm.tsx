/**
 * Task creation form component with validation.
 *
 * Features:
 * - Zod schema validation
 * - Real-time error display
 * - Accessible form inputs
 * - Auto-clear on successful submit
 */
"use client";

import { useState } from "react";
import { taskCreateSchema, TaskCreateFormData } from "@/lib/validators";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

interface TaskFormProps {
  onSubmit: (data: TaskCreateFormData) => Promise<void>;
}

export function TaskForm({ onSubmit }: TaskFormProps) {
  const [formData, setFormData] = useState<TaskCreateFormData>({
    title: "",
    description: "",
  });

  const [errors, setErrors] = useState<Partial<Record<keyof TaskCreateFormData, string>>>({});
  const [loading, setLoading] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  /**
   * Handle input change
   */
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear field error when user starts typing
    if (errors[name as keyof TaskCreateFormData]) {
      setErrors((prev) => ({
        ...prev,
        [name]: undefined,
      }));
    }

    // Clear submit error
    if (submitError) {
      setSubmitError(null);
    }
  };

  /**
   * Handle form submission
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate with Zod
    const result = taskCreateSchema.safeParse(formData);

    if (!result.success) {
      // Extract field errors from Zod
      const fieldErrors: Partial<Record<keyof TaskCreateFormData, string>> = {};
      result.error.errors.forEach((err) => {
        const field = err.path[0] as keyof TaskCreateFormData;
        fieldErrors[field] = err.message;
      });
      setErrors(fieldErrors);
      return;
    }

    try {
      setLoading(true);
      setSubmitError(null);

      await onSubmit(result.data);

      // Clear form on success
      setFormData({ title: "", description: "" });
      setErrors({});
    } catch (err: any) {
      const errorMessage = err.message || "Failed to create task. Please try again.";
      setSubmitError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow-sm rounded-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Create New Task</h2>

      {/* Global error */}
      {submitError && (
        <div
          className="mb-4 p-4 text-sm text-red-800 bg-red-100 border border-red-200 rounded-lg"
          role="alert"
        >
          {submitError}
        </div>
      )}

      <div className="space-y-4">
        {/* Title field */}
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title
          </label>
          <Input
            id="title"
            name="title"
            type="text"
            value={formData.title}
            onChange={handleChange}
            error={errors.title}
            placeholder="What needs to be done?"
            autoComplete="off"
            required
          />
          {errors.title && (
            <p className="mt-1 text-sm text-red-600" role="alert">
              {errors.title}
            </p>
          )}
        </div>

        {/* Description field */}
        <div>
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Description (optional)
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Add more details..."
            rows={3}
            maxLength={1000}
            className={`block w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
              errors.description ? "border-red-500" : "border-gray-300"
            }`}
          />
          {errors.description && (
            <p className="mt-1 text-sm text-red-600" role="alert">
              {errors.description}
            </p>
          )}
        </div>

        {/* Submit button */}
        <Button
          type="submit"
          variant="primary"
          className="w-full"
          disabled={loading}
          aria-label="Create task"
        >
          {loading ? "Creating..." : "Create Task"}
        </Button>
      </div>
    </form>
  );
}
