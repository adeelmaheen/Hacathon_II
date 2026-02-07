'use client';

/** Task card component for displaying individual tasks with advanced features */
import type { Task, Priority } from '@/types';
import { useState } from 'react';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
}

const getPriorityColor = (priority: Priority) => {
  switch (priority) {
    case 'low': return 'bg-gray-100 text-gray-700 border-gray-300';
    case 'medium': return 'bg-blue-100 text-blue-700 border-blue-300';
    case 'high': return 'bg-orange-100 text-orange-700 border-orange-300';
    case 'urgent': return 'bg-red-100 text-red-700 border-red-300';
  }
};

const getPriorityBadge = (priority: Priority) => {
  switch (priority) {
    case 'low': return '⚪ Low';
    case 'medium': return '🔵 Medium';
    case 'high': return '🟠 High';
    case 'urgent': return '🔴 Urgent';
  }
};

export default function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const tags = task.tags || [];

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      setIsDeleting(true);
      await onDelete(task.id);
      setIsDeleting(false);
    }
  };

  const formatDate = (dateString: string | null | undefined) => {
    if (!dateString) return null;
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const formatDateTime = (dateString: string | null | undefined) => {
    if (!dateString) return null;
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const isOverdue = task.due_date && !task.completed && new Date(task.due_date) < new Date();

  return (
    <div
      className={`bg-white rounded-lg shadow-md p-4 border-l-4 ${
        task.completed
          ? 'border-green-500 opacity-75'
          : isOverdue
          ? 'border-red-500'
          : 'border-blue-500'
      } ${isDeleting ? 'opacity-50' : ''}`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggleComplete(task.id)}
              className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
            />
            <h3
              className={`text-lg font-semibold ${
                task.completed ? 'line-through text-gray-500' : 'text-gray-800'
              }`}
            >
              {task.title}
            </h3>
            <span
              className={`px-2 py-1 rounded text-xs font-medium border ${getPriorityColor(
                task.priority || 'medium'
              )}`}
            >
              {getPriorityBadge(task.priority || 'medium')}
            </span>
            {isOverdue && !task.completed && (
              <span className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs font-medium">
                ⚠ Overdue
              </span>
            )}
            {task.recurrence_pattern && (
              <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs font-medium">
                🔁 {task.recurrence_pattern}
              </span>
            )}
          </div>
          
          {task.description && (
            <p
              className={`text-sm text-gray-600 ml-7 mb-2 ${
                task.completed ? 'line-through' : ''
              }`}
            >
              {task.description}
            </p>
          )}

          {/* Tags */}
          {tags.length > 0 && (
            <div className="flex flex-wrap gap-1 ml-7 mb-2">
              {tags.map((tag) => (
                <span
                  key={tag}
                  className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}

          {/* Due Date and Reminder */}
          <div className="ml-7 space-y-1">
            {task.due_date && (
              <p className="text-xs text-gray-600">
                📅 Due: {formatDate(task.due_date)}
                {isOverdue && !task.completed && (
                  <span className="text-red-600 font-medium"> (Overdue)</span>
                )}
              </p>
            )}
            {task.reminder_time && (
              <p className="text-xs text-gray-500">
                ⏰ Reminder: {formatDateTime(task.reminder_time)}
              </p>
            )}
            {task.next_due_date && task.recurrence_pattern && (
              <p className="text-xs text-purple-600">
                🔁 Next: {formatDate(task.next_due_date)}
              </p>
            )}
          </div>

          <p className="text-xs text-gray-400 mt-2 ml-7">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="flex gap-2 ml-4">
          <button
            onClick={() => onEdit(task)}
            disabled={task.completed}
            className={`px-3 py-1 text-sm rounded ${
              task.completed
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50"
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
    </div>
  );
}
