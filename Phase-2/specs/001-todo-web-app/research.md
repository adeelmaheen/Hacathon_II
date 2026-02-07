# Research: Full-Stack Todo Web Application

**Feature**: 001-todo-web-app
**Date**: 2026-01-01
**Purpose**: Technology decisions, best practices, and architectural patterns for implementation

## Overview

This document consolidates research findings and architectural decisions for building a full-stack todo application with excellent UX, responsive design, and clean modular code structure. All decisions align with project constitution and specification requirements.

---

## 1. Authentication Architecture

### Decision: JWT with HTTPOnly Cookies + localStorage Hybrid

**Rationale**:
- **Security**: HTTPOnly cookies prevent XSS attacks on token storage
- **UX**: localStorage enables token persistence across tabs/windows
- **Hybrid Approach**: Use HTTPOnly cookie for token storage, localStorage for client-side user state
- **Refresh Strategy**: Single 24-hour token (refresh tokens out of scope for MVP)

**Implementation Pattern**:
```typescript
// Frontend: lib/auth.ts
export const authClient = {
  async login(email: string, password: string) {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include' // Include cookies
    })
    const data = await response.json()
    localStorage.setItem('user', JSON.stringify(data.user)) // User info only
    return data
  },

  logout() {
    localStorage.removeItem('user')
    // Cookie cleared via API call
  }
}
```

**Backend Pattern** (FastAPI):
```python
# Backend: api/auth.py
@router.post("/login")
async def login(credentials: LoginRequest, response: Response):
    user = await authenticate_user(credentials.email, credentials.password)
    token = create_access_token(user.id)

    # Set HTTPOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax",
        max_age=86400  # 24 hours
    )

    return {"user": {"id": user.id, "name": user.name, "email": user.email}}
```

**Alternatives Considered**:
- **localStorage only**: Rejected due to XSS vulnerability
- **Session-based auth**: Rejected due to server-side state requirement (reduces scalability)
- **Refresh tokens**: Deferred to future iteration (adds complexity for MVP)

**Dependencies**:
- Backend: `python-jose[cryptography]` for JWT, `bcrypt` for password hashing
- Frontend: Native fetch API, no additional JWT library needed

---

## 2. Form Validation Strategy

### Decision: Dual Validation with Zod (Frontend) + Pydantic (Backend)

**Rationale**:
- **Consistency**: Pydantic models define canonical validation rules
- **UX**: Client-side validation with Zod provides immediate feedback
- **Security**: Server-side validation with Pydantic prevents bypass
- **Type Safety**: Both libraries provide TypeScript/Python type generation

**Frontend Validation Pattern** (Zod):
```typescript
// frontend/src/lib/validators.ts
import { z } from 'zod'

export const taskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be under 200 characters'),
  description: z.string()
    .max(1000, 'Description must be under 1000 characters')
    .optional()
})

export type TaskFormData = z.infer<typeof taskSchema>
```

**Backend Validation Pattern** (Pydantic):
```python
# backend/src/schemas/task.py
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
```

**Validation Synchronization**:
- Maintain matching validation rules in Zod and Pydantic
- Character limits, required fields, formats must align
- Document validation rules in API contracts (openapi.yaml)

**Alternatives Considered**:
- **Client-side only**: Rejected (security risk, can be bypassed)
- **Server-side only**: Rejected (poor UX, slow feedback)
- **React Hook Form without Zod**: Rejected (less type safety)

**Dependencies**:
- Frontend: `zod@3.22+` for schema validation
- Backend: Pydantic 2.5+ (included with FastAPI)

---

## 3. State Management Approach

### Decision: React Hooks + Context API (No Redux)

**Rationale**:
- **Simplicity**: Application state is minimal (user auth + task list)
- **Built-in**: React Context API sufficient for global state
- **Performance**: Server Components reduce client-side state needs
- **Avoid Over-engineering**: Redux adds complexity without clear benefit for this scope

**State Architecture**:

1. **Authentication State** (Context):
   ```typescript
   // frontend/src/hooks/useAuth.tsx
   const AuthContext = createContext<AuthContextType | null>(null)

   export function AuthProvider({ children }: { children: ReactNode }) {
     const [user, setUser] = useState<User | null>(() => {
       const stored = localStorage.getItem('user')
       return stored ? JSON.parse(stored) : null
     })

     const login = async (email: string, password: string) => {
       const data = await authClient.login(email, password)
       setUser(data.user)
     }

     return (
       <AuthContext.Provider value={{ user, login, logout }}>
         {children}
       </AuthContext.Provider>
     )
   }
   ```

2. **Task State** (Local Component State + SWR for fetching):
   ```typescript
   // frontend/src/hooks/useTasks.tsx
   import useSWR from 'swr'

   export function useTasks() {
     const { data, error, mutate } = useSWR('/api/tasks', fetcher)

     const createTask = async (task: TaskCreate) => {
       await api.createTask(task)
       mutate() // Revalidate task list
     }

     return { tasks: data, isLoading: !data && !error, createTask, ... }
   }
   ```

**State Breakdown**:
- **Global State**: User authentication (Context API)
- **Server State**: Tasks, user profile (SWR with cache)
- **UI State**: Filters, sorts, modals (local useState)
- **Form State**: React Hook Form with Zod validation

**Alternatives Considered**:
- **Redux/Redux Toolkit**: Rejected (overkill for simple state)
- **Zustand**: Rejected (unnecessary third-party dependency)
- **React Query**: Considered but SWR preferred (simpler API, smaller bundle)

**Dependencies**:
- Frontend: `swr@2.2+` for data fetching/caching
- Frontend: `react-hook-form@7.49+` for form state

---

## 4. Responsive Design Implementation

### Decision: Mobile-First with Tailwind CSS Breakpoints

**Rationale**:
- **Mobile-First**: Design for smallest screen first, enhance for larger screens
- **Tailwind Breakpoints**: Provides consistent responsive utilities
- **Touch Optimization**: Minimum 44x44px touch targets on mobile
- **Flexbox + Grid**: Modern CSS layout for flexible components

**Breakpoint Strategy**:
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'sm': '640px',   // Small tablets portrait
      'md': '768px',   // Tablets landscape, small laptops
      'lg': '1024px',  // Desktops
      'xl': '1280px',  // Large desktops
      '2xl': '1536px'  // Ultra-wide displays
    }
  }
}
```

**Component Patterns**:
```tsx
// Responsive task card
<div className="
  w-full                    /* Full width on mobile */
  p-4                       /* Consistent padding */
  md:w-1/2                  /* 50% width on tablets */
  lg:w-1/3                  /* 33% width on desktop */
  min-h-[44px]              /* Minimum touch target */
">
  <button className="
    w-full h-12             /* Full width, 48px height (>44px) */
    text-sm md:text-base    /* Smaller text on mobile */
    px-4 py-2
  ">
    Mark Complete
  </button>
</div>
```

**Touch Optimization**:
- All interactive elements minimum 44x44px (iOS guideline)
- Adequate spacing between clickable elements (8px minimum)
- Larger tap targets on mobile breakpoints
- Prevent accidental clicks with confirmation dialogs (delete action)

**Typography Scale**:
```css
/* Mobile-first typography */
h1: text-2xl md:text-4xl    /* 24px -> 36px */
h2: text-xl md:text-2xl     /* 20px -> 24px */
body: text-sm md:text-base  /* 14px -> 16px */
```

**Alternatives Considered**:
- **Desktop-First**: Rejected (mobile usage dominant, harder to optimize down)
- **CSS Modules**: Rejected (Tailwind more consistent, faster development)
- **Styled Components**: Rejected (runtime cost, larger bundle)

**Dependencies**:
- Frontend: `tailwindcss@3.4+`, `@tailwindcss/forms@0.5+`
- Frontend: `autoprefixer@10+` for browser compatibility

---

## 5. API Design Pattern

### Decision: REST with OpenAPI 3.0 Specification

**Rationale**:
- **Standard**: REST is well-understood and widely supported
- **Tooling**: FastAPI auto-generates OpenAPI docs
- **Validation**: OpenAPI enables contract testing
- **Simplicity**: No need for GraphQL complexity for CRUD operations

**Endpoint Structure**:
```
Authentication:
POST   /api/auth/register      → Create user account
POST   /api/auth/login         → Get authentication token
POST   /api/auth/logout        → Clear authentication

Tasks:
GET    /api/tasks              → List user's tasks (?status=pending|completed&sort=created|title)
POST   /api/tasks              → Create new task
GET    /api/tasks/{id}         → Get specific task
PUT    /api/tasks/{id}         → Update task
DELETE /api/tasks/{id}         → Delete task
PATCH  /api/tasks/{id}/toggle  → Toggle completion status
```

**Response Format** (Consistent Structure):
```json
// Success (2xx)
{
  "id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-01T10:00:00Z"
}

// Error (4xx/5xx)
{
  "detail": "Task not found"
}
```

**Pagination** (Future Consideration):
- Not required for MVP (assume <500 tasks per user)
- If needed: Add `?limit=50&offset=0` query parameters
- Response includes `total`, `limit`, `offset` fields

**Alternatives Considered**:
- **GraphQL**: Rejected (overkill for simple CRUD, adds complexity)
- **RPC-style**: Rejected (less conventional, harder to cache)
- **HATEOAS**: Rejected (unnecessary for single-page application)

**Dependencies**:
- Backend: FastAPI (includes OpenAPI generation)
- Contract Validation: `openapi-spec-validator@0.7+` (optional)

---

## 6. Database Migration Strategy

### Decision: Alembic with SQLModel Integration

**Rationale**:
- **Alembic**: Industry-standard migration tool for SQLAlchemy/SQLModel
- **Version Control**: Migration scripts tracked in git
- **Reversibility**: All migrations support upgrade/downgrade
- **Team Coordination**: Prevents schema drift across environments

**Migration Workflow**:
```bash
# 1. Create migration after model change
alembic revision --autogenerate -m "add tasks table"

# 2. Review generated migration script
# Edit alembic/versions/xxx_add_tasks_table.py

# 3. Apply migration
alembic upgrade head

# 4. Rollback if needed
alembic downgrade -1
```

**Initial Migration** (users + tasks):
```python
# alembic/versions/001_initial_schema.py
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.String(1000)),
        sa.Column('completed', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now())
    )

    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_completed', 'tasks', ['completed'])
```

**Alternatives Considered**:
- **Manual SQL scripts**: Rejected (error-prone, no rollback support)
- **SQLModel auto-create**: Rejected (no migration history, dangerous in production)
- **Django migrations**: Rejected (Python framework lock-in)

**Dependencies**:
- Backend: `alembic@1.13+`
- Backend: `psycopg2-binary@2.9+` (PostgreSQL adapter)

---

## 7. Error Handling Strategy

### Decision: Centralized Error Boundaries + Consistent API Errors

**Rationale**:
- **User Experience**: All errors show user-friendly messages
- **Consistency**: Same error format across all endpoints
- **Debugging**: Errors logged with context for troubleshooting
- **Recovery**: UI provides retry mechanisms for transient failures

**Backend Error Handling**:
```python
# backend/src/api/deps.py
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail="Authentication service unavailable")
```

**Frontend Error Boundary**:
```typescript
// frontend/src/components/ErrorBoundary.tsx
export function ErrorBoundary({ children }: { children: ReactNode }) {
  const [hasError, setHasError] = useState(false)

  useEffect(() => {
    const handleError = (error: ErrorEvent) => {
      console.error('Global error:', error)
      setHasError(true)
    }
    window.addEventListener('error', handleError)
    return () => window.removeEventListener('error', handleError)
  }, [])

  if (hasError) {
    return (
      <div className="error-state">
        <h2>Something went wrong</h2>
        <button onClick={() => window.location.reload()}>Reload Page</button>
      </div>
    )
  }

  return <>{children}</>
}
```

**API Client Error Handling**:
```typescript
// frontend/src/lib/api.ts
async function handleResponse(response: Response) {
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'An error occurred')
  }
  return response.json()
}

export const api = {
  async getTasks() {
    try {
      const response = await fetch('/api/tasks', { credentials: 'include' })
      return await handleResponse(response)
    } catch (error) {
      // Show user-friendly toast notification
      toast.error(error.message)
      throw error
    }
  }
}
```

**Error Categories**:
- **401 Unauthorized**: Redirect to login page
- **403 Forbidden**: Show "Access denied" message
- **404 Not Found**: Show "Resource not found" with navigation options
- **422 Validation Error**: Show field-specific error messages
- **500 Server Error**: Show generic error with retry button
- **Network Error**: Show "Connection lost" with retry button

**Alternatives Considered**:
- **Error codes instead of messages**: Rejected (poor UX, requires translation)
- **Stack traces in production**: Rejected (security risk, confusing to users)
- **Silent failures**: Rejected (users need feedback)

**Dependencies**:
- Frontend: `react-hot-toast@2.4+` for toast notifications
- Backend: Python `logging` module (built-in)

---

## 8. Accessibility Implementation

### Decision: WCAG 2.1 Level AA Compliance with ARIA

**Rationale**:
- **Legal**: WCAG AA is standard for accessibility compliance
- **Inclusive**: Ensures usability for users with disabilities
- **SEO**: Semantic HTML improves search engine indexing
- **Testing**: Lighthouse audits validate accessibility

**Implementation Checklist**:

**Semantic HTML**:
```tsx
<main role="main">
  <h1>My Tasks</h1>
  <nav aria-label="Task filters">
    <button aria-pressed={filter === 'all'}>All Tasks</button>
  </nav>
  <ul role="list" aria-label="Task list">
    <li role="listitem">
      <article aria-labelledby="task-123-title">
        <h2 id="task-123-title">Buy groceries</h2>
      </article>
    </li>
  </ul>
</main>
```

**Keyboard Navigation**:
- Tab order follows visual flow
- Enter/Space activate buttons
- Escape closes modals
- Arrow keys navigate lists (optional enhancement)
- Focus visible styles (outline on focus)

**Screen Reader Support**:
```tsx
// Live regions for dynamic updates
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {message && <span>{message}</span>}
</div>

// ARIA labels for icon buttons
<button aria-label="Delete task" onClick={handleDelete}>
  <TrashIcon aria-hidden="true" />
</button>

// Form labels and error announcements
<label htmlFor="task-title">Task Title</label>
<input id="task-title" aria-describedby="title-error" />
<span id="title-error" role="alert">{error}</span>
```

**Color Contrast** (WCAG AA):
- Text: Minimum 4.5:1 contrast ratio
- Large text (18pt+): Minimum 3:1 contrast ratio
- Interactive elements: Clear focus indicators
- Test with tools: Lighthouse, axe DevTools

**Focus Management**:
```typescript
// Trap focus in modal
export function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (isOpen) {
      const previousFocus = document.activeElement
      modalRef.current?.focus()

      return () => {
        (previousFocus as HTMLElement)?.focus()
      }
    }
  }, [isOpen])

  return (
    <div ref={modalRef} role="dialog" aria-modal="true" tabIndex={-1}>
      {children}
    </div>
  )
}
```

**Alternatives Considered**:
- **WCAG AAA**: Rejected (too strict for MVP, diminishing returns)
- **No ARIA**: Rejected (fails accessibility requirements)
- **Third-party accessibility widgets**: Rejected (poor UX, false sense of compliance)

**Dependencies**:
- Frontend: `@headlessui/react@1.7+` for accessible UI primitives
- Testing: `@axe-core/react@4.8+` (dev dependency)

---

## 9. Performance Optimization

### Decision: Server Components + Optimistic UI Updates

**Rationale**:
- **Server Components**: Reduce JavaScript bundle size, improve initial load
- **Optimistic Updates**: Instant UI feedback before server confirmation
- **Code Splitting**: Load only necessary code per page
- **Image Optimization**: Next.js Image component for responsive images

**Performance Strategies**:

**1. Server Components (Default)**:
```tsx
// app/dashboard/page.tsx (Server Component)
export default async function DashboardPage() {
  const tasks = await getTasks() // Server-side fetch
  return <TaskList tasks={tasks} />
}
```

**2. Client Components (Interactive Only)**:
```tsx
// components/TaskCard.tsx (Client Component)
'use client'
export function TaskCard({ task }: { task: Task }) {
  const [isCompleted, setIsCompleted] = useState(task.completed)

  const handleToggle = async () => {
    setIsCompleted(!isCompleted) // Optimistic update
    try {
      await api.toggleTask(task.id)
    } catch {
      setIsCompleted(isCompleted) // Revert on error
      toast.error('Failed to update task')
    }
  }

  return <div>...</div>
}
```

**3. Code Splitting**:
```tsx
// Lazy load modal (only when needed)
const TaskModal = dynamic(() => import('@/components/TaskModal'), {
  loading: () => <Spinner />,
  ssr: false // Client-side only
})
```

**4. Bundle Optimization**:
```javascript
// next.config.js
module.exports = {
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['lucide-react', 'date-fns']
  },
  webpack: (config) => {
    config.optimization.splitChunks = {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          priority: -10
        }
      }
    }
    return config
  }
}
```

**Performance Budget**:
- Initial bundle: <300KB (gzipped)
- Time to Interactive: <3s on 3G
- Largest Contentful Paint: <2.5s
- Cumulative Layout Shift: <0.1

**Alternatives Considered**:
- **Client-side rendering only**: Rejected (slower initial load, poor SEO)
- **Service workers for caching**: Deferred to future iteration (adds complexity)
- **CDN for API**: Rejected (not beneficial for dynamic content)

**Dependencies**:
- Frontend: Next.js 14 (includes optimization features)
- Frontend: `next/image` for image optimization

---

## 10. Development Environment Setup

### Decision: Docker Compose for Local Development

**Rationale**:
- **Consistency**: Same environment across all developers
- **Isolation**: No conflicts with local system dependencies
- **Database**: PostgreSQL container included
- **Hot Reload**: Both frontend and backend support live reloading

**Docker Compose Configuration**:
```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: todoapp
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    command: uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://dev:devpass123@db:5432/todoapp
      JWT_SECRET_KEY: dev-secret-key-change-in-production
    depends_on:
      - db

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
```

**Quick Start Commands**:
```bash
# Start all services
docker-compose up

# Start specific service
docker-compose up backend

# View logs
docker-compose logs -f backend

# Run migrations
docker-compose exec backend alembic upgrade head

# Access database
docker-compose exec db psql -U dev -d todoapp
```

**Alternatives Considered**:
- **Local installation**: Rejected (inconsistent environments, setup overhead)
- **Kubernetes**: Rejected (overkill for local development)
- **Vagrant**: Rejected (heavier than Docker, slower)

**Dependencies**:
- Docker Desktop 4.0+ or Docker Engine 20.0+
- Docker Compose 2.0+

---

## Summary

All technology decisions align with project constitution and specification requirements. The research phase is complete with clear implementation patterns for:

1. ✅ JWT authentication with HTTPOnly cookies
2. ✅ Dual validation (Zod + Pydantic)
3. ✅ React Hooks + Context (no Redux)
4. ✅ Mobile-first responsive design with Tailwind
5. ✅ REST API with OpenAPI specification
6. ✅ Alembic database migrations
7. ✅ Centralized error handling
8. ✅ WCAG 2.1 AA accessibility
9. ✅ Server Components + optimistic UI
10. ✅ Docker Compose development environment

**Next Step**: Proceed to Phase 1 (Design & Contracts) to generate data models, API contracts, and quickstart guide.
