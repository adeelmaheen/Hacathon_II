# Frontend Guidelines - Next.js 14

This file provides frontend-specific context for Claude Code when working in the `/frontend` directory.

## Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **State Management**: React hooks (useState, useContext)
- **API Client**: Custom client in `/lib/api.ts`

## Architecture Patterns

### Server Components First

- **Default**: Use Server Components for all pages and layouts
- **Performance**: Server Components reduce bundle size and improve initial load
- **When to use Client Components**:
  - Interactive features (onClick, onChange, form submissions)
  - Browser-only APIs (localStorage, window)
  - React hooks (useState, useEffect, useContext)
  - Event listeners

**Example**:
```tsx
// app/page.tsx - Server Component (default)
export default async function HomePage() {
  const tasks = await api.getTasks()
  return <TaskList tasks={tasks} />
}

// components/TaskList.tsx - Client Component (interactive)
'use client'
import { useState } from 'react'
export function TaskList({ tasks }) {
  const [filter, setFilter] = useState('all')
  // ... interactive logic
}
```

### API Client Pattern

All backend API calls MUST go through `/lib/api.ts`:

```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = {
  async getTasks() {
    const res = await fetch(`${API_BASE}/api/tasks`, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
    if (!res.ok) throw new Error('Failed to fetch tasks')
    return res.json()
  },
  // ... other methods
}
```

**Benefits**:
- Centralized error handling
- Consistent auth token management
- Easy to mock for testing
- Type safety across the app

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js 14 App Router pages
│   │   ├── layout.tsx    # Root layout
│   │   ├── page.tsx      # Home page
│   │   └── tasks/        # Task pages
│   ├── components/       # Reusable UI components
│   │   ├── TaskCard.tsx
│   │   └── Header.tsx
│   └── lib/              # Utilities and API client
│       ├── api.ts        # Backend API client
│       └── utils.ts      # Helper functions
├── public/               # Static assets
├── package.json
└── tsconfig.json
```

## Styling Guidelines

### Tailwind CSS

- **Use utility classes**: `className="flex items-center gap-4"`
- **NO inline styles**: Avoid `style={{ ... }}`
- **Follow existing patterns**: Check other components for consistency
- **Responsive design**: Use `sm:`, `md:`, `lg:` prefixes

**Example**:
```tsx
<div className="max-w-4xl mx-auto p-6">
  <h1 className="text-3xl font-bold text-gray-900 mb-4">
    My Tasks
  </h1>
  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
    {/* Task cards */}
  </div>
</div>
```

### Component Conventions

- **Naming**: PascalCase for components (`TaskCard.tsx`)
- **Props**: Destructure with TypeScript types
- **Exports**: Named exports for components

```tsx
// components/TaskCard.tsx
interface TaskCardProps {
  title: string
  completed: boolean
  onToggle: () => void
}

export function TaskCard({ title, completed, onToggle }: TaskCardProps) {
  return (
    <div className="p-4 border rounded-lg">
      <h3 className="font-medium">{title}</h3>
      <button onClick={onToggle}>
        {completed ? 'Mark Incomplete' : 'Mark Complete'}
      </button>
    </div>
  )
}
```

## TypeScript Standards

- **Strict mode**: Enabled in `tsconfig.json`
- **NO `any` types**: Use proper types or `unknown`
- **Interface over type**: Use `interface` for object shapes
- **Type imports**: Use `import type` when importing types only

```typescript
// Good
interface User {
  id: string
  email: string
  name: string
}

// Avoid
type User = {
  id: any  // ❌ NO any types
  email: string
}
```

## Authentication

- **JWT tokens**: Stored in httpOnly cookies or localStorage
- **Protected routes**: Use middleware or layout checks
- **Token refresh**: Handle token expiration gracefully

```typescript
// lib/api.ts
function getToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('auth_token')
}

export const api = {
  async getTasks() {
    const token = getToken()
    if (!token) throw new Error('Not authenticated')

    const res = await fetch(`${API_BASE}/api/tasks`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return res.json()
  }
}
```

## Error Handling

- **User-friendly messages**: Show clear error states in UI
- **Loading states**: Always show loading indicators
- **Fallbacks**: Provide fallback UI for errors

```tsx
'use client'
export function TaskList() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.getTasks()
      .then(setTasks)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div>Loading tasks...</div>
  if (error) return <div>Error: {error.message}</div>

  return <div>{/* Render tasks */}</div>
}
```

## Development Workflow

### Running the Dev Server

```bash
cd frontend
npm install
npm run dev
```

Access at: `http://localhost:3000`

### Building for Production

```bash
npm run build
npm start
```

### Linting & Formatting

```bash
npm run lint
npm run format
```

## Key Conventions

1. **Specs First**: Always read `/specs/features/`, `/specs/ui/`, `/specs/api/` before implementing
2. **Reference Specs**: Use `@specs/features/task-crud.md` syntax in prompts
3. **Consistent Patterns**: Follow existing component structure
4. **Small Commits**: Commit after each logical component or feature
5. **Constitution Compliance**: Follow principles in `.specify/memory/constitution.md`

## Common Tasks

### Creating a New Page

1. Read UI spec: `@specs/ui/pages.md`
2. Create page in `app/[route]/page.tsx`
3. Use Server Component by default
4. Extract interactive parts to Client Components

### Creating a Reusable Component

1. Read UI spec: `@specs/ui/components.md`
2. Create in `components/[ComponentName].tsx`
3. Define TypeScript interface for props
4. Use Tailwind for styling
5. Export as named export

### Adding an API Call

1. Read API spec: `@specs/api/rest-endpoints.md`
2. Add method to `lib/api.ts`
3. Include auth token handling
4. Handle errors appropriately
5. Use in components via the API client

## References

- Root instructions: `@/CLAUDE.md`
- Constitution: `@.specify/memory/constitution.md`
- Backend API: `@backend/CLAUDE.md`
- Specs: `@specs/`
