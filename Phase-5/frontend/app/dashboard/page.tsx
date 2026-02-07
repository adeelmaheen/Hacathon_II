'use client';

/** Dashboard page for managing tasks with advanced features */
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { auth } from '@/lib/auth';
import { taskAPI } from '@/lib/api';
import type { Task, User, SortBy, SortOrder, Priority } from '@/types';
import TaskCard from '@/components/ui/task-card';
import TaskForm, { TaskFormData } from '@/components/ui/task-form';

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [error, setError] = useState('');

  // Search, Filter, Sort state
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'completed' | 'pending'>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('');
  const [tagFilter, setTagFilter] = useState('');
  const [sortBy, setSortBy] = useState<SortBy>('created_at');
  const [sortOrder, setSortOrder] = useState<SortOrder>('desc');

  useEffect(() => {
    // Check authentication
    if (!auth.isAuthenticated()) {
      router.push('/');
      return;
    }

    // Get user from storage
    const storedUser = auth.getUser();
    if (storedUser) {
      setUser(storedUser);
      loadTasks(storedUser.id);
    } else {
      router.push('/');
    }
  }, [router]);

  const loadTasks = async (userId: number) => {
    try {
      setIsLoading(true);
      setError('');
      
      // Use combined endpoint for search, filter, and sort
      const options: any = {
        sort_by: sortBy,
        order: sortOrder,
      };
      
      if (searchQuery) {
        options.q = searchQuery;
      }
      
      if (statusFilter !== 'all') {
        options.status = statusFilter;
      }
      
      if (priorityFilter) {
        options.priority = priorityFilter;
      }
      
      if (tagFilter) {
        options.tag = tagFilter;
      }
      
      const data = await taskAPI.combined(userId, options);
      setTasks(data);
    } catch (err: any) {
      setError('Failed to load tasks. Please try again.');
      console.error('Error loading tasks:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      loadTasks(user.id);
    }
  }, [searchQuery, statusFilter, priorityFilter, tagFilter, sortBy, sortOrder, user]);

  const handleAddTask = async (data: TaskFormData) => {
    if (!user) return;

    try {
      await taskAPI.create(user.id, data);
      await loadTasks(user.id);
      setIsFormOpen(false);
    } catch (err: any) {
      throw err; // Let TaskForm handle the error
    }
  };

  const handleEditTask = async (data: TaskFormData) => {
    if (!user || !editingTask) return;

    try {
      await taskAPI.update(user.id, editingTask.id, data);
      await loadTasks(user.id);
      setEditingTask(null);
      setIsFormOpen(false);
    } catch (err: any) {
      throw err; // Let TaskForm handle the error
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    if (!user) return;

    try {
      await taskAPI.toggleComplete(user.id, taskId);
      await loadTasks(user.id);
    } catch (err: any) {
      setError('Failed to update task. Please try again.');
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!user) return;

    try {
      await taskAPI.delete(user.id, taskId);
      await loadTasks(user.id);
    } catch (err: any) {
      setError('Failed to delete task. Please try again.');
    }
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setIsFormOpen(true);
  };

  const handleCancel = () => {
    setEditingTask(null);
    setIsFormOpen(false);
  };

  const handleLogout = () => {
    auth.clearAuth();
    router.push('/');
  };

  // Get all unique tags from tasks
  const allTags = Array.from(
    new Set(tasks.flatMap((task) => task.tags || []))
  ).sort();

  if (!user) {
    return null; // Will redirect
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">My Tasks</h1>
              <p className="text-gray-600 mt-1">Welcome back, {user.name}!</p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => router.push('/chat')}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                💬 Chat Assistant
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
              >
                Logout
              </button>
            </div>
          </div>
        </div>

        {/* Error message */}
        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Search, Filter, Sort Panel */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Search */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                🔍 Search
              </label>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search tasks..."
                className="w-full border border-gray-300 rounded px-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Status Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as any)}
                className="w-full border border-gray-300 rounded px-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Tasks</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            {/* Priority Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Priority
              </label>
              <select
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value)}
                className="w-full border border-gray-300 rounded px-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Priorities</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>

            {/* Tag Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tag
              </label>
              <select
                value={tagFilter}
                onChange={(e) => setTagFilter(e.target.value)}
                className="w-full border border-gray-300 rounded px-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Tags</option>
                {allTags.map((tag) => (
                  <option key={tag} value={tag}>
                    #{tag}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Sort Controls */}
          <div className="mt-4 flex gap-4 items-end">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Sort By
              </label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as SortBy)}
                className="w-full border border-gray-300 rounded px-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="created_at">Created Date</option>
                <option value="due_date">Due Date</option>
                <option value="priority">Priority</option>
                <option value="title">Title</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Order
              </label>
              <select
                value={sortOrder}
                onChange={(e) => setSortOrder(e.target.value as SortOrder)}
                className="w-full border border-gray-300 rounded px-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="desc">Descending</option>
                <option value="asc">Ascending</option>
              </select>
            </div>
            <button
              onClick={() => {
                setSearchQuery('');
                setStatusFilter('all');
                setPriorityFilter('');
                setTagFilter('');
                setSortBy('created_at');
                setSortOrder('desc');
              }}
              className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
            >
              Clear Filters
            </button>
          </div>
        </div>

        {/* Add Task Button */}
        {!isFormOpen && (
          <button
            onClick={() => {
              setEditingTask(null);
              setIsFormOpen(true);
            }}
            className="mb-4 w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 font-medium shadow-md"
          >
            + Add New Task
          </button>
        )}

        {/* Task Form */}
        {isFormOpen && (
          <TaskForm
            task={editingTask}
            onSubmit={editingTask ? handleEditTask : handleAddTask}
            onCancel={handleCancel}
          />
        )}

        {/* Tasks List */}
        {isLoading ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Loading tasks...</p>
          </div>
        ) : tasks.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <p className="text-gray-600 text-lg">
              {searchQuery || statusFilter !== 'all' || priorityFilter || tagFilter
                ? 'No tasks match your filters. Try adjusting your search criteria.'
                : 'No tasks yet. Create your first task!'}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onToggleComplete={handleToggleComplete}
                onEdit={handleEdit}
                onDelete={handleDeleteTask}
              />
            ))}
          </div>
        )}

        {/* Stats */}
        {tasks.length > 0 && (
          <div className="mt-6 bg-white rounded-lg shadow-md p-4">
            <div className="flex justify-around text-center">
              <div>
                <p className="text-2xl font-bold text-gray-800">{tasks.length}</p>
                <p className="text-sm text-gray-600">Total Tasks</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-green-600">
                  {tasks.filter((t) => t.completed).length}
                </p>
                <p className="text-sm text-gray-600">Completed</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-blue-600">
                  {tasks.filter((t) => !t.completed).length}
                </p>
                <p className="text-sm text-gray-600">Pending</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-red-600">
                  {tasks.filter((t) => t.due_date && !t.completed && new Date(t.due_date) < new Date()).length}
                </p>
                <p className="text-sm text-gray-600">Overdue</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
