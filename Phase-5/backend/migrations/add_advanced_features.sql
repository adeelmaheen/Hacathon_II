-- Migration: Add advanced features to tasks table
-- Phase V: Advanced Cloud Deployment

-- Add new columns to tasks table
ALTER TABLE task ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium';
ALTER TABLE task ADD COLUMN IF NOT EXISTS tags TEXT;
ALTER TABLE task ADD COLUMN IF NOT EXISTS due_date TIMESTAMP;
ALTER TABLE task ADD COLUMN IF NOT EXISTS reminder_time TIMESTAMP;
ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(50);
ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_interval INTEGER;
ALTER TABLE task ADD COLUMN IF NOT EXISTS next_due_date TIMESTAMP;
ALTER TABLE task ADD COLUMN IF NOT EXISTS parent_task_id INTEGER REFERENCES task(id);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_task_priority ON task(priority);
CREATE INDEX IF NOT EXISTS idx_task_due_date ON task(due_date);
CREATE INDEX IF NOT EXISTS idx_task_created_at ON task(created_at);
CREATE INDEX IF NOT EXISTS idx_task_title ON task(title);
CREATE INDEX IF NOT EXISTS idx_task_completed ON task(completed);

-- Create recurring_tasks table (lowercase to match SQLModel)
CREATE TABLE IF NOT EXISTS recurringtask (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL UNIQUE REFERENCES task(id) ON DELETE CASCADE,
    pattern VARCHAR(50) NOT NULL,
    interval INTEGER NOT NULL DEFAULT 1,
    last_created_at TIMESTAMP,
    next_due_date TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_recurringtask_task_id ON recurringtask(task_id);
CREATE INDEX IF NOT EXISTS idx_recurringtask_next_due_date ON recurringtask(next_due_date);
CREATE INDEX IF NOT EXISTS idx_recurringtask_is_active ON recurringtask(is_active);

-- Create reminders table
CREATE TABLE IF NOT EXISTS reminder (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES task(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    remind_at TIMESTAMP NOT NULL,
    sent BOOLEAN NOT NULL DEFAULT FALSE,
    sent_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reminder_task_id ON reminder(task_id);
CREATE INDEX IF NOT EXISTS idx_reminder_user_id ON reminder(user_id);
CREATE INDEX IF NOT EXISTS idx_reminder_remind_at ON reminder(remind_at);
CREATE INDEX IF NOT EXISTS idx_reminder_sent ON reminder(sent);

-- Add comments for documentation
COMMENT ON COLUMN task.priority IS 'Task priority: low, medium, high, urgent';
COMMENT ON COLUMN task.tags IS 'JSON array of tag strings';
COMMENT ON COLUMN task.due_date IS 'When the task is due';
COMMENT ON COLUMN task.reminder_time IS 'When to send reminder before due date';
COMMENT ON COLUMN task.recurrence_pattern IS 'Recurrence pattern: daily, weekly, monthly, yearly, custom';
COMMENT ON COLUMN task.recurrence_interval IS 'Recurrence interval (e.g., every 2 days)';
COMMENT ON COLUMN task.next_due_date IS 'Next occurrence due date for recurring tasks';
COMMENT ON COLUMN task.parent_task_id IS 'Reference to parent task in recurring task chain';

