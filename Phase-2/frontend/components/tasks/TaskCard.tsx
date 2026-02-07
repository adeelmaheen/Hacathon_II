/**
 * Task card component for displaying individual tasks.
 *
 * Features:
 * - Shows title and description (if present)
 * - Checkbox for completion toggle
 * - Delete button with confirmation
 * - Formatted creation date
 * - Accessible markup
 */
"use client";

import { useState } from "react";
import { Task, TaskUpdate } from "@/types/task";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

interface TaskCardProps {
  task: Task;
  onToggle: (taskId: number) => Promise<void>;
  onUpdate: (taskId: number, data: TaskUpdate) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
}

export function TaskCard({ task, onToggle, onUpdate, onDelete }: TaskCardProps) {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || "");
  const [saving, setSaving] = useState(false);
  const [editError, setEditError] = useState("");

  /**
   * Format date to readable string
   */
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };

  /**
   * Handle checkbox toggle
   */
  const handleToggle = async () => {
    try {
      await onToggle(task.id);
    } catch (err) {
      console.error("Toggle failed:", err);
    }
  };

  /**
   * Handle delete confirmation
   */
  const handleDelete = async () => {
    try {
      setDeleting(true);
      await onDelete(task.id);
      setShowDeleteModal(false);
    } catch (err) {
      console.error("Delete failed:", err);
      setDeleting(false);
    }
  };

  /**
   * Enter edit mode
   */
  const handleEditClick = () => {
    setIsEditing(true);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
    setEditError("");
  };

  /**
   * Cancel edit mode
   */
  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
    setEditError("");
  };

  /**
   * Save edited task
   */
  const handleSaveEdit = async () => {
    // Validate title
    const trimmedTitle = editTitle.trim();
    if (!trimmedTitle) {
      setEditError("Title cannot be empty");
      return;
    }

    if (trimmedTitle.length > 200) {
      setEditError("Title must be 200 characters or less");
      return;
    }

    if (editDescription.length > 1000) {
      setEditError("Description must be 1000 characters or less");
      return;
    }

    try {
      setSaving(true);
      setEditError("");

      await onUpdate(task.id, {
        title: trimmedTitle,
        description: editDescription.trim() || null,
      });

      setIsEditing(false);
    } catch (err) {
      console.error("Update failed:", err);
      setEditError(err instanceof Error ? err.message : "Failed to update task");
      setSaving(false);
    } finally {
      if (!editError) {
        setSaving(false);
      }
    }
  };

  return (
    <>
      <div
        className={`bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow ${
          task.completed ? "opacity-75" : ""
        }`}
      >
        {isEditing ? (
          /* Edit Mode */
          <div className="space-y-3">
            {/* Title Input */}
            <div>
              <label htmlFor={`edit-title-${task.id}`} className="block text-sm font-medium text-gray-700 mb-1">
                Title
              </label>
              <Input
                id={`edit-title-${task.id}`}
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                disabled={saving}
                className="w-full"
                maxLength={200}
              />
            </div>

            {/* Description Input */}
            <div>
              <label htmlFor={`edit-description-${task.id}`} className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                id={`edit-description-${task.id}`}
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                disabled={saving}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                rows={3}
                maxLength={1000}
              />
            </div>

            {/* Error Message */}
            {editError && (
              <p className="text-sm text-red-600">{editError}</p>
            )}

            {/* Action Buttons */}
            <div className="flex gap-2 justify-end">
              <Button
                variant="secondary"
                onClick={handleCancelEdit}
                disabled={saving}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                onClick={handleSaveEdit}
                disabled={saving}
              >
                {saving ? "Saving..." : "Save"}
              </Button>
            </div>
          </div>
        ) : (
          /* Display Mode */
          <div className="flex items-start gap-3">
            {/* Completion checkbox */}
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggle}
              className="mt-1 w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500 cursor-pointer"
              aria-label={`Mark "${task.title}" as ${task.completed ? "incomplete" : "complete"}`}
            />

            <div className="flex-1">
              <h3
                className={`text-lg font-medium text-gray-900 ${
                  task.completed ? "line-through text-gray-500" : ""
                }`}
              >
                {task.title}
              </h3>

              {/* Description - only show if present */}
              {task.description && (
                <p className="mt-2 text-sm text-gray-600 whitespace-pre-wrap">
                  {task.description}
                </p>
              )}

              {/* Creation date */}
              <p className="mt-2 text-xs text-gray-500">
                Created {formatDate(task.created_at)}
              </p>
            </div>

            {/* Edit button */}
            <button
              onClick={handleEditClick}
              className="text-blue-600 hover:text-blue-800 p-1 rounded hover:bg-blue-50 transition-colors"
              aria-label={`Edit "${task.title}"`}
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </button>

            {/* Delete button */}
            <button
              onClick={() => setShowDeleteModal(true)}
              className="text-red-600 hover:text-red-800 p-1 rounded hover:bg-red-50 transition-colors"
              aria-label={`Delete "${task.title}"`}
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </div>
        )}
      </div>

      {/* Delete confirmation modal */}
      {showDeleteModal && (
        <Modal
          isOpen={showDeleteModal}
          onClose={() => setShowDeleteModal(false)}
          title="Delete Task"
        >
          <div className="space-y-4">
            <p className="text-gray-700">
              Are you sure you want to delete "{task.title}"? This action cannot be undone.
            </p>

            <div className="flex gap-3 justify-end">
              <Button
                variant="secondary"
                onClick={() => setShowDeleteModal(false)}
                disabled={deleting}
              >
                Cancel
              </Button>
              <Button
                variant="danger"
                onClick={handleDelete}
                disabled={deleting}
              >
                {deleting ? "Deleting..." : "Delete"}
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </>
  );
}
