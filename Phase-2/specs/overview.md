# Hackathon II: Todo App - Project Overview

## Purpose

A full-stack todo application built using spec-driven development methodology that evolves through three phases:
- **Phase 1**: Console application (CLI-based task management)
- **Phase 2**: Full-stack web application (Next.js + FastAPI)
- **Phase 3**: AI-powered chatbot interface

## Current Phase

**Phase 2**: Full-Stack Web Application

Building a modern web interface with user authentication and database persistence.

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **State Management**: React hooks
- **Authentication**: Better Auth (client-side)

### Backend
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL
- **Authentication**: Better Auth with JWT
- **Validation**: Pydantic models
- **Python Version**: 3.11+

### Infrastructure
- **Monorepo**: Single repository with frontend/backend separation
- **Package Managers**: npm (frontend), pip (backend)
- **Containerization**: Docker Compose
- **Version Control**: Git with feature branches

## Features

### Phase 1 (Console) - Completed
- [x] Basic task CRUD operations
- [x] CLI interface for task management
- [x] Local file storage

### Phase 2 (Web) - In Progress
- [ ] User authentication and authorization
- [ ] Task CRUD operations (web interface)
- [ ] User-scoped task management
- [ ] Task filtering and sorting
- [ ] PostgreSQL database persistence
- [ ] RESTful API endpoints
- [ ] Responsive web UI

### Phase 3 (Chatbot) - Planned
- [ ] AI chatbot interface
- [ ] Natural language task creation
- [ ] Conversational task management
- [ ] Smart task suggestions
- [ ] Integration with existing web interface

## Development Methodology

### Spec-Driven Development

Every feature follows a structured workflow:

1. **Specification** (`/sp.specify`) - Define requirements and user stories
2. **Planning** (`/sp.plan`) - Design architecture and technical approach
3. **Tasks** (`/sp.tasks`) - Generate actionable task list
4. **Implementation** (`/sp.implement`) - Execute tasks
5. **Review** - Validate against acceptance criteria

### Documentation Structure

```
specs/
├── overview.md          # This file - project overview
├── architecture.md      # System architecture and design
├── features/            # Feature specifications
│   ├── task-crud.md     # Task CRUD operations
│   ├── authentication.md # User authentication
│   └── chatbot.md       # AI chatbot (Phase 3)
├── api/                 # API contracts
│   ├── rest-endpoints.md # REST API documentation
│   └── mcp-tools.md     # MCP tools (Phase 3)
├── database/            # Database specifications
│   └── schema.md        # Database schema and models
└── ui/                  # UI specifications
    ├── components.md    # Reusable components
    └── pages.md         # Page layouts and flows
```

## Success Criteria

### Phase 2 Goals

- Users can create accounts and log in securely
- Authenticated users can perform full CRUD on tasks
- Tasks are persisted in PostgreSQL database
- Each user sees only their own tasks
- UI is responsive and works on mobile devices
- API follows RESTful conventions
- All endpoints require authentication (except auth routes)

### Quality Metrics

- **Performance**: API response time < 200ms (p95)
- **Security**: All passwords hashed, JWT tokens used, HTTPS enforced
- **Reliability**: 99% uptime, graceful error handling
- **Usability**: Task creation in < 3 clicks, intuitive navigation

## Project Governance

All development follows the project constitution at `.specify/memory/constitution.md`, which defines:
- Core development principles
- Technology standards
- Development workflow
- Compliance requirements

## Getting Started

### Prerequisites

- Node.js 18+ (frontend)
- Python 3.11+ (backend)
- PostgreSQL (Neon account or local)
- Docker (optional, for containerized development)

### Development Setup

1. Clone repository
2. Install dependencies:
   ```bash
   # Frontend
   cd frontend && npm install

   # Backend
   cd backend && pip install -r requirements.txt
   ```
3. Configure environment variables (`.env` files)
4. Run development servers:
   ```bash
   # Frontend (port 3000)
   cd frontend && npm run dev

   # Backend (port 8000)
   cd backend && uvicorn src.main:app --reload
   ```

### With Docker Compose

```bash
docker-compose up
```

## Links

- **Repository**: (Add GitHub URL)
- **Constitution**: `.specify/memory/constitution.md`
- **Spec-Kit Config**: `.spec-kit/config.yaml`
- **Frontend Docs**: `frontend/CLAUDE.md`
- **Backend Docs**: `backend/CLAUDE.md`

## Team

- **Developer**: Maheen-Arif
- **Project**: Hackathon II - Spec-Driven Development
- **Started**: 2026-01-01

---

*Last Updated*: 2026-01-01
