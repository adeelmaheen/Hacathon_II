/**
 * Task filters component for filtering and sorting tasks.
 *
 * Features:
 * - Status filter dropdown (all/pending/completed)
 * - Sort by dropdown (created/title)
 * - Sort order dropdown (asc/desc)
 * - Connected to useTasks hook state
 */
"use client";

import { TaskFilters as TaskFiltersType, TaskStatus, TaskSortBy, TaskSortOrder } from "@/types/task";

interface TaskFiltersProps {
  filters: TaskFiltersType;
  onChange: (filters: TaskFiltersType) => void;
}

export function TaskFilters({ filters, onChange }: TaskFiltersProps) {
  const handleStatusChange = (status: TaskStatus) => {
    onChange({ ...filters, status });
  };

  const handleSortChange = (sort: TaskSortBy) => {
    onChange({ ...filters, sort });
  };

  const handleOrderChange = (order: TaskSortOrder) => {
    onChange({ ...filters, order });
  };

  return (
    <div className="bg-white border rounded-lg p-4 shadow-sm">
      <div className="flex flex-col sm:flex-row gap-4">
        {/* Status Filter */}
        <div className="flex-1">
          <label
            htmlFor="status-filter"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Status
          </label>
          <select
            id="status-filter"
            value={filters.status}
            onChange={(e) => handleStatusChange(e.target.value as TaskStatus)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Tasks</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        {/* Sort By */}
        <div className="flex-1">
          <label
            htmlFor="sort-filter"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Sort By
          </label>
          <select
            id="sort-filter"
            value={filters.sort}
            onChange={(e) => handleSortChange(e.target.value as TaskSortBy)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="created">Date Created</option>
            <option value="title">Title</option>
          </select>
        </div>

        {/* Sort Order */}
        <div className="flex-1">
          <label
            htmlFor="order-filter"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Order
          </label>
          <select
            id="order-filter"
            value={filters.order}
            onChange={(e) => handleOrderChange(e.target.value as TaskSortOrder)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="desc">Newest First</option>
            <option value="asc">Oldest First</option>
          </select>
        </div>
      </div>
    </div>
  );
}
