/**
 * Empty state component shown when user has no tasks.
 *
 * Features:
 * - Friendly encouragement message
 * - Visual icon placeholder
 * - Context-aware messages based on filter
 */
"use client";

import { TaskStatus } from "@/types/task";

interface EmptyStateProps {
  status?: TaskStatus;
}

export function EmptyState({ status = "all" }: EmptyStateProps) {
  const getEmptyMessage = () => {
    switch (status) {
      case "completed":
        return {
          title: "No completed tasks",
          description: "Tasks you mark as complete will appear here. Keep up the great work!",
        };
      case "pending":
        return {
          title: "No pending tasks",
          description: "You're all caught up! All your tasks are complete.",
        };
      default:
        return {
          title: "No tasks yet",
          description: "Get started by creating your first task above. Stay organized and accomplish your goals!",
        };
    }
  };

  const { title, description } = getEmptyMessage();

  return (
    <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
      {/* Icon placeholder */}
      <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
        <svg
          className="w-8 h-8 text-blue-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
      </div>

      {/* Message */}
      <h3 className="text-lg font-medium text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-600 max-w-sm mx-auto">{description}</p>
    </div>
  );
}
