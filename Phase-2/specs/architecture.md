# System Architecture

## Overview

Hackathon II is a full-stack todo application built using a **monorepo architecture** with clear separation between frontend and backend services. The system follows **spec-driven development** principles and uses modern web technologies.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Client (Browser)                     │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Next.js 14 Frontend (Port 3000)          │   │
│  │                                                   │   │
│  │  • Server Components (SSR)                       │   │
│  │  • Client Components (Interactive UI)            │   │
│  │  • Tailwind CSS (Styling)                        │   │
│  │  • TypeScript (Type Safety)                      │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                                │
│                         │ HTTPS / Fetch API              │
│                         ▼                                │
└─────────────────────────────────────────────────────────┘
                          │
                          │ JWT Token in Authorization Header
                          ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                 │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │               API Layer                          │   │
│  │  • /api/auth (Login, Register, Token)           │   │
│  │  • /api/tasks (CRUD operations)                 │   │
│  │  • Pydantic Validation                          │   │
│  │  • JWT Authentication Middleware                │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                                │
│                         ▼                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │            Business Logic Layer                  │   │
│  │  • Task Service (CRUD logic)                    │   │
│  │  • Auth Service (User management)               │   │
│  │  • User isolation enforcement                   │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                                │
│                         ▼                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Data Access Layer                   │   │
│  │  • SQLModel ORM                                  │   │
│  │  • Database session management                   │   │
│  │  • Query optimization                            │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                                │
└─────────────────────────────────────────────────────────┘
                          │
                          │ PostgreSQL Protocol
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Neon PostgreSQL Database                    │
│                                                           │
│  Tables:                                                  │
│  • users (id, email, name, password_hash)               │
│  • tasks (id, user_id, title, description, completed)   │
│                                                           │
│  Indexes:                                                 │
│  • tasks.user_id (filter by user)                       │
│  • tasks.completed (filter by status)                   │
└─────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend (Next.js 14)

**Location**: `/frontend`

**Responsibilities**:
- Render user interface (Server + Client components)
- Handle user interactions and form submissions
- Manage client-side state (React hooks)
- Communicate with backend API
- Store and manage JWT authentication tokens

**Key Files**:
- `app/` - Next.js App Router pages and layouts
- `components/` - Reusable UI components
- `lib/api.ts` - Centralized API client for backend communication

**Technology Choices**:
- **Next.js 14 App Router**: Server-first rendering for performance, SEO
- **TypeScript**: Type safety and developer experience
- **Tailwind CSS**: Utility-first styling, rapid UI development

### Backend (FastAPI)

**Location**: `/backend`

**Responsibilities**:
- Expose RESTful API endpoints
- Validate incoming requests (Pydantic models)
- Authenticate and authorize users (JWT)
- Execute business logic
- Interact with database (SQLModel ORM)
- Return JSON responses

**Key Files**:
- `main.py` - FastAPI application entry point
- `api/` - Route handlers organized by resource
- `services/` - Business logic layer
- `models/` - SQLModel database models
- `db.py` - Database connection management

**Technology Choices**:
- **FastAPI**: Modern, fast, auto-generated OpenAPI docs
- **SQLModel**: Type-safe ORM combining SQLAlchemy + Pydantic
- **Better Auth**: Production-ready JWT authentication

### Database (Neon PostgreSQL)

**Location**: Cloud-hosted (Neon)

**Responsibilities**:
- Persist user accounts and task data
- Enforce data integrity (foreign keys, constraints)
- Provide indexed queries for fast retrieval
- Support ACID transactions

**Schema**:
- `users` table - User accounts (managed by Better Auth)
- `tasks` table - User tasks with foreign key to users

**Indexes**:
- Primary keys (auto-indexed)
- Foreign key `tasks.user_id` for user filtering
- `tasks.completed` for status filtering

## Data Flow

### User Registration Flow

```
User submits form → Frontend validates → POST /api/auth/register
→ Backend validates (Pydantic) → Hash password → Insert into users table
→ Return success → Frontend redirects to login
```

### Task Creation Flow

```
User submits task → Frontend sends POST /api/tasks with JWT token
→ Backend validates JWT → Extract user_id from token
→ Validate task data (Pydantic) → Create Task with user_id
→ Insert into database → Return task object → Frontend updates UI
```

### Task Retrieval Flow

```
User loads page → Frontend sends GET /api/tasks with JWT token
→ Backend validates JWT → Extract user_id from token
→ Query tasks WHERE user_id = ? → Return filtered tasks
→ Frontend renders task list
```

## Security Architecture

### Authentication Flow

1. **Registration**: User provides email/password → Backend hashes password → Stores in database
2. **Login**: User provides credentials → Backend verifies → Issues JWT token → Frontend stores token
3. **Authorized Requests**: Frontend sends JWT in `Authorization: Bearer <token>` header → Backend validates → Extracts user context → Processes request

### Security Principles

- **Password Security**: Bcrypt hashing with salt, never stored in plaintext
- **JWT Tokens**: Signed with secret key, include user_id in payload, expiration timestamp
- **User Isolation**: All queries filtered by authenticated user_id from JWT
- **HTTPS**: All production traffic encrypted (enforced at deployment)
- **Environment Secrets**: API keys, database URLs, JWT secrets stored in `.env` (not committed)

### Authorization Model

- **Public Endpoints**: `/api/auth/register`, `/api/auth/login`
- **Protected Endpoints**: All `/api/tasks/*` routes require valid JWT
- **User Scope**: Users can only access their own tasks (enforced at service layer)

## Monorepo Organization

### Directory Structure

```
Phase-2/
├── .spec-kit/              # Spec-Kit configuration
│   └── config.yaml
├── specs/                  # Specifications (Spec-Kit managed)
│   ├── overview.md
│   ├── architecture.md     # This file
│   ├── features/
│   ├── api/
│   ├── database/
│   └── ui/
├── frontend/               # Next.js application
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   ├── CLAUDE.md
│   └── package.json
├── backend/                # FastAPI application
│   ├── src/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   ├── tests/
│   ├── CLAUDE.md
│   └── requirements.txt
├── history/                # Development history
│   ├── prompts/            # Prompt History Records
│   └── adr/                # Architecture Decision Records
├── .specify/               # SpecKit Plus templates
│   ├── memory/
│   │   └── constitution.md
│   └── templates/
├── CLAUDE.md               # Root Claude Code instructions
└── docker-compose.yml      # Container orchestration
```

### Benefits of Monorepo

- **Atomic Changes**: Update frontend and backend in single commit
- **Shared Types**: Can share TypeScript/Python type definitions
- **Unified Tooling**: Single CI/CD pipeline, consistent linting
- **Simplified Specs**: Specs reference both frontend and backend in one place
- **Claude Code Context**: Single context for cross-stack changes

## API Design

### RESTful Conventions

- **Base URL**: `http://localhost:8000` (dev), `https://api.example.com` (prod)
- **Prefix**: All routes under `/api/`
- **Content-Type**: `application/json`
- **Authentication**: `Authorization: Bearer <jwt-token>` header

### Endpoint Structure

```
POST   /api/auth/register       # Create user account
POST   /api/auth/login          # Get JWT token
GET    /api/tasks               # List user's tasks
POST   /api/tasks               # Create new task
GET    /api/tasks/{id}          # Get specific task
PUT    /api/tasks/{id}          # Update task
DELETE /api/tasks/{id}          # Delete task
PATCH  /api/tasks/{id}/complete # Toggle completion status
```

### Response Format

**Success** (200 OK):
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-01T10:00:00Z"
}
```

**Error** (4xx/5xx):
```json
{
  "detail": "Task not found"
}
```

## Deployment Architecture

### Development Environment

- Frontend: `npm run dev` on port 3000
- Backend: `uvicorn main:app --reload` on port 8000
- Database: Neon cloud instance

### Production Environment (Planned)

- Frontend: Vercel (Next.js deployment)
- Backend: Railway or Render (FastAPI deployment)
- Database: Neon PostgreSQL (production instance)
- HTTPS: Enforced at platform level

### Environment Configuration

**Frontend** (`.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend** (`.env`):
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

## Scalability Considerations

### Current Phase (Phase 2)

- Single server architecture
- Suitable for 100-1000 users
- No caching layer (database query optimization only)
- Synchronous request handling

### Future Optimizations (Phase 3+)

- **Caching**: Redis for frequently accessed tasks
- **Database**: Read replicas for query scaling
- **CDN**: Static asset caching for frontend
- **Load Balancing**: Multiple backend instances
- **Background Jobs**: Celery for async task processing

## Testing Strategy

### Frontend Tests

- **Unit**: Component testing with Jest/React Testing Library
- **Integration**: User flow testing with Playwright/Cypress
- **E2E**: Full user journeys from login to task management

### Backend Tests

- **Contract**: API endpoint validation against specs
- **Integration**: Database operations and service layer
- **Unit**: Business logic in service layer

## Observability

### Logging

- **Frontend**: Browser console (dev), error tracking service (prod)
- **Backend**: Structured JSON logs, request/response logging
- **Database**: Query logging (development only)

### Monitoring (Planned)

- API endpoint performance metrics
- Error rates and stack traces
- User activity analytics

## References

- **Constitution**: `.specify/memory/constitution.md`
- **Spec-Kit Config**: `.spec-kit/config.yaml`
- **Frontend Guidelines**: `frontend/CLAUDE.md`
- **Backend Guidelines**: `backend/CLAUDE.md`
- **API Specs**: `specs/api/rest-endpoints.md` (to be created)
- **Database Schema**: `specs/database/schema.md` (to be created)

---

*Last Updated*: 2026-01-01
