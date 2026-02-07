/**
 * Dashboard page (authenticated)
 *
 * Main landing page for authenticated users showing their tasks.
 * Features:
 * - Task creation form
 * - Task list (or empty state)
 * - Real-time updates with SWR
 */
"use client";

import { useTasks } from "@/hooks/useTasks";
import { TaskForm } from "@/components/tasks/TaskForm";
import { TaskFilters } from "@/components/tasks/TaskFilters";
import { TaskList } from "@/components/tasks/TaskList";

export default function DashboardPage() {
  const { tasks, loading, error, filters, setFilters, createTask, updateTask, toggleTask, deleteTask } = useTasks();

  return (
    <div className="space-y-6">
      {/* Task creation form */}
      <TaskForm onSubmit={createTask} />

      {/* Task filters */}
      <TaskFilters filters={filters} onChange={setFilters} />

      {/* Task list or empty state */}
      <TaskList
        tasks={tasks}
        loading={loading}
        error={error}
        status={filters.status}
        onToggle={toggleTask}
        onUpdate={updateTask}
        onDelete={deleteTask}
      />
    </div>
  );
}
