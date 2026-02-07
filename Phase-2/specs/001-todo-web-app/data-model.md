# Data Model: Full-Stack Todo Web Application

**Feature**: 001-todo-web-app
**Date**: 2026-01-01
**Purpose**: Define entity models, validation rules, and database schema

## Overview

This document defines the data entities, relationships, validation rules, and state transitions for the todo application. All models support the functional requirements (FR-001 to FR-030) and enforce data integrity, user isolation, and security constraints.

---

## Entity Diagram

```
┌─────────────────────────────┐
│          User               │
│─────────────────────────────│
│ id: String (PK, UUID)       │
│ email: String (UNIQUE)      │
│ name: String                │
│ password_hash: String       │
│ created_at: DateTime        │
└─────────────────────────────┘
          │
          │ 1
          │
          │ owns
          │
          │ N
          ▼
┌─────────────────────────────┐
│          Task               │
│─────────────────────────────│
│ id: Integer (PK, AUTO)      │
│ user_id: String (FK)        │
│ title: String(200)          │
│ description: String(1000)?  │
│ completed: Boolean          │
│ created_at: DateTime        │
│ updated_at: DateTime        │
└─────────────────────────────┘
```

**Relationship**: One User owns many Tasks (1:N)

---

## 1. User Entity

### Purpose

Represents a registered user account. Each user has unique credentials and owns a collection of tasks. Users are isolated from each other - they can only access their own tasks.

### Attributes

| Attribute      | Type     | Constraints                      | Description                                    |
|----------------|----------|----------------------------------|------------------------------------------------|
| `id`           | String   | PRIMARY KEY, UUID v4             | Unique identifier (not auto-increment for security) |
| `email`        | String   | UNIQUE, NOT NULL, max 255        | User's email address (used for login)         |
| `name`         | String   | NOT NULL, max 100                | User's display name                            |
| `password_hash`| String   | NOT NULL, fixed 60               | Bcrypt hashed password (never plaintext)      |
| `created_at`   | DateTime | NOT NULL, default NOW()          | Account creation timestamp                     |

### Validation Rules

**Email Validation**:
- Format: Standard email regex `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Uniqueness: Case-insensitive check (normalize to lowercase before storage)
- Example: `user@example.com`, `john.doe+tag@company.co.uk`

**Name Validation**:
- Length: 1-100 characters
- Content: Any Unicode characters (supports international names)
- No whitespace-only names
- Example: `John Doe`, `María García`, `李明`

**Password Validation** (before hashing):
- Minimum length: 8 characters (FR-003)
- Maximum length: 72 characters (bcrypt limit)
- No specific character requirements (allows passphrases)
- Example: `mypassword123`, `correct horse battery staple`

**Password Hashing**:
- Algorithm: bcrypt with 12 rounds
- Output: 60-character hash string
- Never store plaintext passwords (FR-029)

### Backend Model (SQLModel)

```python
# backend/src/models/user.py
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        sa_column_kwargs={"nullable": False}
    )
    name: str = Field(
        max_length=100,
        sa_column_kwargs={"nullable": False}
    )
    password_hash: str = Field(
        max_length=60,
        sa_column_kwargs={"nullable": False}
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False}
    )
```

### Frontend Type (TypeScript)

```typescript
// frontend/src/types/user.ts

/**
 * User entity (public fields only - password_hash never exposed)
 */
export interface User {
  id: string
  email: string
  name: string
  created_at: string // ISO 8601 datetime
}

/**
 * Registration payload (before hashing)
 */
export interface RegisterRequest {
  email: string
  name: string
  password: string // Plaintext, hashed on backend
}

/**
 * Login payload
 */
export interface LoginRequest {
  email: string
  password: string
}
```

### Indexes

- `email` (UNIQUE INDEX): Fast lookup during login
- `id` (PRIMARY KEY): Automatic index

### Security Notes

- **Password Storage**: NEVER store plaintext passwords. Always hash with bcrypt before INSERT/UPDATE.
- **User Enumeration**: Login errors should not reveal whether email exists (generic "Invalid credentials" message).
- **Email Normalization**: Convert email to lowercase before uniqueness check to prevent duplicates like `User@Example.com` and `user@example.com`.

---

## 2. Task Entity

### Purpose

Represents a single todo item belonging to a user. Tasks have a title, optional description, completion status, and timestamps. Each task is scoped to exactly one user (enforced via `user_id` foreign key).

### Attributes

| Attribute      | Type     | Constraints                      | Description                                    |
|----------------|----------|----------------------------------|------------------------------------------------|
| `id`           | Integer  | PRIMARY KEY, AUTO INCREMENT      | Unique task identifier                         |
| `user_id`      | String   | FOREIGN KEY → users.id, INDEX    | Owner of this task (enforces user isolation)  |
| `title`        | String   | NOT NULL, max 200                | Task title (required)                          |
| `description`  | String?  | NULLABLE, max 1000               | Optional task description                      |
| `completed`    | Boolean  | NOT NULL, default FALSE, INDEX   | Completion status (pending/completed)         |
| `created_at`   | DateTime | NOT NULL, default NOW()          | Task creation timestamp                        |
| `updated_at`   | DateTime | NOT NULL, default NOW(), ON UPDATE | Last modification timestamp                   |

### Validation Rules

**Title Validation** (FR-008):
- Length: 1-200 characters (required)
- Content: Any Unicode characters
- No whitespace-only titles
- Example: `Buy groceries`, `Call mom`, `🎉 Celebrate birthday`

**Description Validation** (FR-009):
- Length: 0-1000 characters (optional)
- Content: Any Unicode characters including newlines
- Can be null/empty
- Example: `Milk, eggs, bread`, `Remember to buy organic`

**Completed Validation**:
- Type: Boolean (true/false)
- Default: false (new tasks are pending)
- Toggle: Can switch between true/false (FR-012)

### Backend Model (SQLModel)

```python
# backend/src/models/task.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(
        default=None,
        primary_key=True
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        sa_column_kwargs={"nullable": False}
    )
    title: str = Field(
        max_length=200,
        sa_column_kwargs={"nullable": False}
    )
    description: str | None = Field(
        default=None,
        max_length=1000
    )
    completed: bool = Field(
        default=False,
        index=True,
        sa_column_kwargs={"nullable": False}
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "nullable": False,
            "onupdate": datetime.utcnow
        }
    )
```

### Frontend Type (TypeScript)

```typescript
// frontend/src/types/task.ts

/**
 * Task entity (complete representation)
 */
export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string // ISO 8601 datetime
  updated_at: string // ISO 8601 datetime
}

/**
 * Create task payload
 */
export interface TaskCreate {
  title: string
  description?: string | null
}

/**
 * Update task payload (all fields optional)
 */
export interface TaskUpdate {
  title?: string
  description?: string | null
  completed?: boolean
}

/**
 * Task list filters
 */
export type TaskStatus = 'all' | 'pending' | 'completed'
export type TaskSortBy = 'created' | 'title'
export type TaskSortOrder = 'asc' | 'desc'

export interface TaskFilters {
  status?: TaskStatus
  sortBy?: TaskSortBy
  order?: TaskSortOrder
}
```

### Indexes

- `id` (PRIMARY KEY): Automatic index
- `user_id` (INDEX): Fast lookup for user's tasks (FR-011)
- `completed` (INDEX): Fast filtering by status (FR-015)
- Composite index `(user_id, completed)`: Optimize common query pattern

### Foreign Key Constraints

- `user_id` → `users.id`: ON DELETE CASCADE (deleting user deletes all their tasks)
- Prevents orphaned tasks
- Enforces referential integrity

### State Transitions

```
┌─────────┐
│ Pending │ ← Task created (completed=false)
│ (false) │
└─────────┘
     │
     │ User clicks checkbox (PATCH /api/tasks/{id}/toggle)
     ▼
┌─────────┐
│Complete │ ← completed=true
│ (true)  │
└─────────┘
     │
     │ User clicks checkbox again
     ▼
┌─────────┐
│ Pending │ ← Back to completed=false
│ (false) │
└─────────┘
```

**Valid Transitions**:
- `false → true`: Mark task complete
- `true → false`: Mark task incomplete (undo completion)
- No other states exist in v1

### Security Notes

- **User Isolation**: ALL queries MUST filter by `user_id` from authenticated JWT token (FR-011).
- **Authorization**: Users can only CRUD their own tasks. Attempting to access another user's task returns 404 (not 403, to avoid information leakage).
- **Validation**: Both client and server MUST validate title/description length (FR-030).

---

## 3. Derived Data (No Storage)

### Task Statistics

Computed on-the-fly, not stored in database:

```typescript
interface TaskStats {
  total: number           // Count of all tasks
  pending: number         // Count where completed=false
  completed: number       // Count where completed=true
  completionRate: number  // completed / total (percentage)
}
```

**Backend Computation** (if needed):
```python
# Can be added to dashboard endpoint
stats = {
    "total": session.query(Task).filter(Task.user_id == user_id).count(),
    "pending": session.query(Task).filter(Task.user_id == user_id, Task.completed == False).count(),
    "completed": session.query(Task).filter(Task.user_id == user_id, Task.completed == True).count()
}
stats["completion_rate"] = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
```

### Filter/Sort Results

Filtering and sorting are query-time operations, not stored data:

```sql
-- All tasks for user (default: newest first)
SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC;

-- Pending tasks only
SELECT * FROM tasks WHERE user_id = ? AND completed = false ORDER BY created_at DESC;

-- Completed tasks only
SELECT * FROM tasks WHERE user_id = ? AND completed = true ORDER BY created_at DESC;

-- Sort by title (alphabetical)
SELECT * FROM tasks WHERE user_id = ? ORDER BY title ASC;
```

---

## 4. Database Schema (PostgreSQL)

### SQL DDL (for reference - Alembic generates migrations)

```sql
-- Create users table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,  -- UUID
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_users_email ON users(email);

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_tasks_user_id ON tasks(user_id);
CREATE INDEX ix_tasks_completed ON tasks(completed);
CREATE INDEX ix_tasks_user_completed ON tasks(user_id, completed);
```

### Database Size Estimates

**Assumptions**:
- 1000 users
- Average 50 tasks per user
- Average title: 30 characters
- Average description: 100 characters (50% have descriptions)

**User Table**:
- Row size: ~400 bytes (UUID + email + name + hash + timestamp)
- 1000 users × 400 bytes = ~400 KB

**Tasks Table**:
- Row size: ~300 bytes (id + user_id + title + description + booleans + timestamps)
- 50,000 tasks × 300 bytes = ~15 MB

**Indexes**:
- ~5 MB additional

**Total**: ~20 MB for initial scale (well within limits)

---

## 5. Data Integrity Rules

### Application-Level Constraints

1. **User Isolation**: Service layer MUST scope all queries by authenticated `user_id`
2. **Title Required**: Task cannot be created or updated with empty/null title
3. **Length Limits**: Enforce max lengths before database layer (better error messages)
4. **Email Uniqueness**: Check before INSERT, handle conflict gracefully
5. **Password Security**: Hash passwords before storing, never expose hashes in responses

### Database-Level Constraints

1. **Primary Keys**: Enforce uniqueness (id columns)
2. **Foreign Keys**: Ensure referential integrity (user_id → users.id)
3. **NOT NULL**: Prevent missing required fields
4. **UNIQUE**: Prevent duplicate emails
5. **DEFAULT**: Ensure completed=false for new tasks
6. **ON UPDATE**: Auto-update `updated_at` timestamp

### Validation Sequence

```
User Input
    ↓
Frontend Validation (Zod)
    ↓
API Request
    ↓
Backend Validation (Pydantic)
    ↓
Service Layer (Business Logic)
    ↓
Database (Constraints)
    ↓
Response to Client
```

---

## 6. Migration Strategy

### Initial Migration (Version 001)

```python
# alembic/versions/001_initial_schema.py
"""Initial schema: users and tasks

Revision ID: 001
Create Date: 2026-01-01
"""

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('password_hash', sa.String(60), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False)
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.String(1000), nullable=True),
        sa.Column('completed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_completed', 'tasks', ['completed'])
    op.create_index('ix_tasks_user_completed', 'tasks', ['user_id', 'completed'])

def downgrade():
    op.drop_index('ix_tasks_user_completed', 'tasks')
    op.drop_index('ix_tasks_completed', 'tasks')
    op.drop_index('ix_tasks_user_id', 'tasks')
    op.drop_table('tasks')
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
```

### Future Migrations (Out of Scope for MVP)

Potential schema changes for future iterations:
- Add `tasks.due_date` column
- Add `tasks.priority` column
- Add `categories` table with many-to-many relationship
- Add `task_tags` junction table
- Add `users.avatar_url` column
- Add `users.email_verified` boolean

---

## Summary

Data model design complete with:

- ✅ **2 Core Entities**: User, Task
- ✅ **1:N Relationship**: One user owns many tasks
- ✅ **Validation Rules**: Email, password, title, description constraints
- ✅ **Security**: User isolation, password hashing, foreign key constraints
- ✅ **Indexes**: Optimized for common query patterns (user_id, completed)
- ✅ **Type Safety**: SQLModel (backend) + TypeScript interfaces (frontend)
- ✅ **Migration Ready**: Alembic migration script provided

**Next Step**: Generate API contracts (OpenAPI specification) based on these data models.
