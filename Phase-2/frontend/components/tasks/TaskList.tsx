/**
 * Task list container component.
 *
 * Features:
 * - Displays all tasks in grid layout
 * - Shows loading state
 * - Shows error state
 * - Responsive grid (1 column mobile, 2 columns desktop)
 */
"use client";

import { Task, TaskUpdate, TaskStatus } from "@/types/task";
import { TaskCard } from "./TaskCard";
import { EmptyState } from "./EmptyState";
import { Spinner } from "@/components/ui/Spinner";

interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  error: Error | null;
  status?: TaskStatus;
  onToggle: (taskId: number) => Promise<void>;
  onUpdate: (taskId: number, data: TaskUpdate) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
}

export function TaskList({ tasks, loading, error, status = "all", onToggle, onUpdate, onDelete }: TaskListProps) {
  // Loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Spinner />
        <span className="ml-3 text-gray-600">Loading tasks...</span>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div
        className="p-4 text-sm text-red-800 bg-red-100 border border-red-200 rounded-lg"
        role="alert"
      >
        <p className="font-semibold">Error loading tasks</p>
        <p className="mt-1">{error.message}</p>
      </div>
    );
  }

  // Empty state
  if (tasks.length === 0) {
    return <EmptyState status={status} />;
  }

  // Task list
  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">
        Your Tasks ({tasks.length})
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onToggle={onToggle}
            onUpdate={onUpdate}
            onDelete={onDelete}
          />
        ))}
      </div>
    </div>
  );
}
