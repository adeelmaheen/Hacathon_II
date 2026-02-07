/**
 * Task type definitions matching backend TaskResponse schema.
 */

export interface Task {
  id: number
  user_id: string // UUID
  title: string
  description: string | null
  completed: boolean
  created_at: string // ISO 8601 date-time
  updated_at: string // ISO 8601 date-time
}

export interface TaskCreate {
  title: string
  description?: string | null
}

export interface TaskUpdate {
  title?: string
  description?: string | null
  completed?: boolean
}

export interface TaskResponse extends Task {}

export type TaskStatus = 'all' | 'pending' | 'completed'
export type TaskSortBy = 'created' | 'title'
export type TaskSortOrder = 'asc' | 'desc'

export interface TaskFilters {
  status: TaskStatus
  sort: TaskSortBy
  order: TaskSortOrder
}
