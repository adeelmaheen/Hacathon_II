'use client';

/** Dashboard page for managing tasks */
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { auth } from '@/lib/auth';
import { taskAPI } from '@/lib/api';
import type { Task, User } from '@/types';
import TaskCard from '@/components/ui/task-card';
import TaskForm from '@/components/ui/task-form';

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [error, setError] = useState('');

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
      const data = await taskAPI.list(userId);
      setTasks(data);
    } catch (err: any) {
      setError('Failed to load tasks. Please try again.');
      console.error('Error loading tasks:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddTask = async (data: { title: string; description: string }) => {
    if (!user) return;

    try {
      await taskAPI.create(user.id, data);
      await loadTasks(user.id);
      setIsFormOpen(false);
    } catch (err: any) {
      throw err; // Let TaskForm handle the error
    }
  };

  const handleEditTask = async (data: { title: string; description: string }) => {
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

  if (!user) {
    return null; // Will redirect
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
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
            <p className="text-gray-600 text-lg">No tasks yet. Create your first task!</p>
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
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

