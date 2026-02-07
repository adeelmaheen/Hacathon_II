# Quickstart Guide: Full-Stack Todo Web Application

**Feature**: 001-todo-web-app
**Date**: 2026-01-01
**Purpose**: Get developers up and running quickly

## Prerequisites

Before starting development, ensure you have:

- **Docker Desktop** 4.0+ or Docker Engine 20.0+ with Docker Compose 2.0+
- **Node.js** 18+ and npm 9+ (for local frontend development without Docker)
- **Python** 3.11+ and pip (for local backend development without Docker)
- **Git** for version control
- **Code Editor**: VS Code recommended (with extensions: ESLint, Prettier, Python, Tailwind CSS IntelliSense)

## Quick Start (Docker Compose - Recommended)

### 1. Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd Phase-2

# Copy environment templates
cp .env.example .env
cp frontend/.env.local.example frontend/.env.local
cp backend/.env.example backend/.env
```

### 2. Configure Environment

Edit `.env` files with your settings:

**Backend (` backend/.env`):**
```bash
DATABASE_URL=postgresql://dev:devpass123@db:5432/todoapp
JWT_SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**Frontend (`frontend/.env.local`):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start All Services

```bash
# Start database, backend, and frontend
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Run Database Migrations

```bash
# Apply initial schema
docker-compose exec backend alembic upgrade head
```

### 5. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Database**: localhost:5432 (user: dev, password: devpass123, db: todoapp)

### 6. Create Test Account

Open http://localhost:3000/register and create an account:
- Name: Test User
- Email: test@example.com
- Password: password123

## Development Workflow

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev

# Run linting
npm run lint

# Build for production
npm run build

# Type checking
npm run type-check
```

**File Structure**:
```
frontend/src/
├── app/                # Next.js pages
├── components/         # UI components
├── lib/                # API client, utilities
├── hooks/              # Custom React hooks
└── types/              # TypeScript definitions
```

### Backend Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server
uvicorn src.main:app --reload --port 8000

# Run linting
black src/
mypy src/

# Create database migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

**File Structure**:
```
backend/src/
├── main.py             # FastAPI app
├── models/             # Database models
├── schemas/            # Request/response schemas
├── services/           # Business logic
├── api/                # Route handlers
└── utils/              # Helpers
```

### Making Changes

1. **Read the spec**: Check `specs/001-todo-web-app/spec.md` for requirements
2. **Update data model**: If needed, modify `specs/001-todo-web-app/data-model.md`
3. **Update contracts**: If API changes, modify `specs/001-todo-web-app/contracts/openapi.yaml`
4. **Implement backend**: Update models, services, and API routes
5. **Implement frontend**: Update components, hooks, and pages
6. **Test manually**: Verify against acceptance criteria in spec
7. **Commit changes**: Use conventional commits (`feat:`, `fix:`, etc.)

## Common Tasks

### Add New API Endpoint

1. Update OpenAPI spec (`contracts/openapi.yaml`)
2. Add Pydantic schema (`backend/src/schemas/`)
3. Implement service logic (`backend/src/services/`)
4. Add route handler (`backend/src/api/`)
5. Update frontend API client (`frontend/src/lib/api.ts`)
6. Use in component with hooks

### Add New UI Component

1. Check UI spec (`specs/ui/components.md` if exists)
2. Create component file (`frontend/src/components/`)
3. Add TypeScript types (`frontend/src/types/`)
4. Implement with Tailwind CSS
5. Ensure accessibility (ARIA labels, semantic HTML)
6. Use in page or parent component

### Database Schema Change

1. Update SQLModel in `backend/src/models/`
2. Generate migration: `alembic revision --autogenerate -m "add column"`
3. Review generated migration file
4. Test upgrade: `alembic upgrade head`
5. Test downgrade: `alembic downgrade -1`
6. Commit migration file

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 3000 (frontend)
lsof -ti:3000 | xargs kill

# Find process using port 8000 (backend)
lsof -ti:8000 | xargs kill

# Or use different ports in docker-compose.yml
```

### Database Connection Failed

```bash
# Restart database container
docker-compose restart db

# Check database logs
docker-compose logs db

# Connect to database directly
docker-compose exec db psql -U dev -d todoapp
```

### Frontend Build Errors

```bash
# Clear Next.js cache
cd frontend
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Backend Import Errors

```bash
# Reinstall Python dependencies
cd backend
pip install --force-reinstall -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

## Testing

### Manual Testing Checklist

Based on acceptance scenarios in `spec.md`:

**User Story 1 - Authentication**:
- [ ] Register new account with valid email
- [ ] Login with correct credentials
- [ ] Logout successfully
- [ ] See error for invalid email format
- [ ] See error for password <8 characters
- [ ] See error for incorrect login credentials

**User Story 2 - Create/View Tasks**:
- [ ] Create task with title only
- [ ] Create task with title and description
- [ ] View all tasks in list
- [ ] See tasks in reverse chronological order
- [ ] See empty state when no tasks

**User Story 3 - Complete/Delete Tasks**:
- [ ] Mark task as complete (visual indication)
- [ ] Unmark completed task
- [ ] Delete task with confirmation
- [ ] Cancel deletion
- [ ] See success message after delete

**User Story 4 - Edit Tasks**:
- [ ] Edit task title and description
- [ ] Cancel edit (changes discarded)
- [ ] See validation error for empty title
- [ ] See updated task in list immediately

**User Story 5 - Filter/Sort**:
- [ ] Filter to show pending tasks only
- [ ] Filter to show completed tasks only
- [ ] Show all tasks
- [ ] Sort by date created (newest/oldest)
- [ ] Sort by title (A-Z)
- [ ] Preferences persist on refresh

**User Story 6 - Responsive Mobile**:
- [ ] Access on mobile phone (no horizontal scroll)
- [ ] All buttons are tappable (44x44px minimum)
- [ ] Rotate device (layout adjusts)
- [ ] Create task on mobile (keyboard appears correctly)
- [ ] All interactions have visual feedback

### Automated Testing (Optional)

If implementing automated tests:

**Backend Tests**:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_auth.py
```

**Frontend Tests**:
```bash
# Run Jest tests
npm test

# Run E2E tests with Playwright
npm run test:e2e
```

## Performance Optimization

### Check Performance

```bash
# Lighthouse audit
npm run lighthouse

# Bundle analysis
cd frontend
npm run build -- --analyze
```

### Performance Targets

- Lighthouse Performance: 90+
- Lighthouse Accessibility: 90+
- Lighthouse Best Practices: 90+
- First Contentful Paint: <1.5s
- Time to Interactive: <3s
- Bundle size (gzipped): <500KB

## Deployment

### Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

### Backend (Railway/Render)

1. Connect GitHub repository
2. Set environment variables (DATABASE_URL, JWT_SECRET_KEY)
3. Deploy from main branch
4. Run migrations: `alembic upgrade head`

### Database (Neon PostgreSQL)

1. Create Neon project
2. Copy connection string
3. Update DATABASE_URL in backend environment
4. Run migrations

## Resources

- **Specification**: `specs/001-todo-web-app/spec.md`
- **Data Model**: `specs/001-todo-web-app/data-model.md`
- **API Contracts**: `specs/001-todo-web-app/contracts/openapi.yaml`
- **Research**: `specs/001-todo-web-app/research.md`
- **Frontend Guidelines**: `frontend/CLAUDE.md`
- **Backend Guidelines**: `backend/CLAUDE.md`
- **Constitution**: `.specify/memory/constitution.md`

## Next Steps

1. Review specification and acceptance criteria
2. Familiarize yourself with project structure
3. Read constitution for development principles
4. Start implementing user stories in priority order (P1 → P2 → P3)
5. Test each user story independently before moving to next

**Happy coding!** 🚀
