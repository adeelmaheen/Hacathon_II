/**
 * Task management hook with SWR for data fetching and caching.
 *
 * Provides:
 * - Task list fetching with automatic caching
 * - Create task method with optimistic updates
 * - Loading and error states
 */
"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import useSWR from "swr";
import { Task, TaskCreate, TaskUpdate, TaskFilters } from "@/types/task";
import * as api from "@/lib/api";

const FILTER_STORAGE_KEY = "task-filters";

const DEFAULT_FILTERS: TaskFilters = {
  status: "all",
  sort: "created",
  order: "desc",
};

interface UseTasksReturn {
  tasks: Task[];
  loading: boolean;
  error: Error | null;
  filters: TaskFilters;
  setFilters: (filters: TaskFilters) => void;
  createTask: (data: TaskCreate) => Promise<void>;
  updateTask: (taskId: number, data: TaskUpdate) => Promise<void>;
  toggleTask: (taskId: number) => Promise<void>;
  deleteTask: (taskId: number) => Promise<void>;
  refresh: () => Promise<void>;
}

export function useTasks(): UseTasksReturn {
  /**
   * Load filters from sessionStorage on mount
   */
  const [filters, setFiltersState] = useState<TaskFilters>(() => {
    if (typeof window === "undefined") return DEFAULT_FILTERS;

    try {
      const stored = sessionStorage.getItem(FILTER_STORAGE_KEY);
      if (stored) {
        return JSON.parse(stored);
      }
    } catch (err) {
      console.error("Failed to load filters from sessionStorage:", err);
    }
    return DEFAULT_FILTERS;
  });

  /**
   * Save filters to sessionStorage when changed
   */
  useEffect(() => {
    if (typeof window === "undefined") return;

    try {
      sessionStorage.setItem(FILTER_STORAGE_KEY, JSON.stringify(filters));
    } catch (err) {
      console.error("Failed to save filters to sessionStorage:", err);
    }
  }, [filters]);

  /**
   * Update filters
   */
  const setFilters = (newFilters: TaskFilters) => {
    setFiltersState(newFilters);
  };

  /**
   * Fetch tasks with SWR caching and filters
   */
  const {
    data: tasks,
    error,
    isLoading,
    mutate,
  } = useSWR<Task[]>(
    ["/api/tasks", filters],
    () => api.getTasks(filters),
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
    }
  );

  /**
   * Create a new task with optimistic UI update
   */
  const createTask = async (data: TaskCreate) => {
    try {
      // Create task on server
      const newTask = await api.createTask(data);

      // Optimistically update local cache
      mutate(
        (currentTasks) => {
          if (!currentTasks) return [newTask];
          // Add new task at the beginning (most recent first)
          return [newTask, ...currentTasks];
        },
        {
          revalidate: false, // Don't refetch immediately
        }
      );

      // Revalidate after a short delay to ensure server sync
      setTimeout(() => mutate(), 500);
    } catch (err) {
      console.error("Create task error:", err);
      throw err;
    }
  };

  /**
   * Update task with optimistic UI update
   */
  const updateTask = async (taskId: number, data: TaskUpdate) => {
    try {
      // Optimistically update local cache
      mutate(
        (currentTasks) => {
          if (!currentTasks) return currentTasks;
          return currentTasks.map((task) =>
            task.id === taskId
              ? { ...task, ...data, updated_at: new Date().toISOString() }
              : task
          );
        },
        { revalidate: false }
      );

      // Update on server
      await api.updateTask(taskId, data);

      // Revalidate to ensure server sync
      mutate();
    } catch (err) {
      console.error("Update task error:", err);
      // Revert optimistic update on error
      mutate();
      throw err;
    }
  };

  /**
   * Debounce timer for toggle operations
   */
  const toggleTimers = useRef<Map<number, NodeJS.Timeout>>(new Map());

  /**
   * Toggle task completion with optimistic UI update and debouncing
   */
  const toggleTask = useCallback(async (taskId: number) => {
    // Clear any existing timer for this task
    const existingTimer = toggleTimers.current.get(taskId);
    if (existingTimer) {
      clearTimeout(existingTimer);
    }

    try {
      // Optimistically update local cache immediately
      mutate(
        (currentTasks) => {
          if (!currentTasks) return currentTasks;
          return currentTasks.map((task) =>
            task.id === taskId
              ? { ...task, completed: !task.completed, updated_at: new Date().toISOString() }
              : task
          );
        },
        { revalidate: false }
      );

      // Debounce the actual API call
      const timer = setTimeout(async () => {
        try {
          await api.toggleTask(taskId);
          mutate();
        } catch (err) {
          console.error("Toggle task error:", err);
          mutate(); // Revert on error
        } finally {
          toggleTimers.current.delete(taskId);
        }
      }, 300); // 300ms debounce

      toggleTimers.current.set(taskId, timer);
    } catch (err) {
      console.error("Toggle task error:", err);
      mutate();
      throw err;
    }
  }, [mutate]);

  /**
   * Delete task with cache invalidation
   */
  const deleteTask = async (taskId: number) => {
    try {
      // Optimistically remove from cache
      mutate(
        (currentTasks) => {
          if (!currentTasks) return currentTasks;
          return currentTasks.filter((task) => task.id !== taskId);
        },
        { revalidate: false }
      );

      // Delete on server
      await api.deleteTask(taskId);

      // Revalidate to ensure server sync
      mutate();
    } catch (err) {
      console.error("Delete task error:", err);
      // Revert optimistic update on error
      mutate();
      throw err;
    }
  };

  return {
    tasks: tasks || [],
    loading: isLoading,
    error: error || null,
    filters,
    setFilters,
    createTask,
    updateTask,
    toggleTask,
    deleteTask,
    refresh: async () => {
      await mutate();
    },
  };
}
