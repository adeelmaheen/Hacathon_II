# Hackathon II: Spec-Driven Development Constitution

<!--
SYNC IMPACT REPORT
==================
Version Change: 0.0.0 → 1.0.0
Rationale: Initial constitution creation with comprehensive principles for full-stack monorepo development

Modified Principles: N/A (initial creation)
Added Sections:
  - Core Principles (7 principles)
  - Technology Standards
  - Development Workflow
  - Governance

Templates Status:
  ✅ plan-template.md - Constitution Check section validated
  ✅ spec-template.md - User scenarios and requirements align
  ✅ tasks-template.md - Task categorization matches principles

Follow-up TODOs: None
-->

## Core Principles

### I. Spec-Driven Development (Non-Negotiable)

All development MUST follow the spec-driven workflow:
- Every feature begins with a specification in `/specs/features/`
- Specifications MUST be written before implementation
- Implementation MUST strictly follow the approved specification
- Changes to requirements MUST update the spec first, then code
- No code changes without corresponding spec documentation

**Rationale**: Ensures alignment between business requirements and implementation, creates single source of truth for feature expectations, and maintains clear project history.

### II. Monorepo Organization

The project MUST maintain clean separation between frontend and backend:
- Frontend code lives in `/frontend` (Next.js 14 with App Router)
- Backend code lives in `/backend` (FastAPI with SQLModel)
- Shared specifications live in `/specs` organized by type (features, api, database, ui)
- Cross-cutting changes MUST update both frontend and backend in the same commit
- Each workspace (frontend/backend) MUST have its own `CLAUDE.md` for context-specific guidance

**Rationale**: Monorepo enables atomic cross-stack changes while maintaining clear boundaries. Spec-Kit integration provides structured specifications that Claude Code can reference effectively.

### III. API-First Design

All backend features MUST follow API-first principles:
- API contracts MUST be defined in `/specs/api/` before implementation
- All routes MUST be under `/api/` prefix
- REST endpoints MUST use Pydantic models for request/response validation
- Authentication MUST be enforced via JWT tokens in Authorization header
- Errors MUST use HTTPException with appropriate status codes
- API responses MUST return JSON with consistent structure

**Rationale**: API-first design ensures frontend and backend can be developed in parallel, provides clear contracts for testing, and maintains consistency across all endpoints.

### IV. Database Schema Management

All data models MUST follow strict schema governance:
- Schema MUST be documented in `/specs/database/schema.md` before implementation
- All database operations MUST use SQLModel ORM (no raw SQL)
- Database connection MUST use environment variable `DATABASE_URL`
- Migrations MUST be reversible and tested
- Schema changes MUST update specification first
- User data MUST be isolated per user (user_id foreign key required)
- Indexes MUST be defined for all foreign keys and frequently filtered columns

**Rationale**: Structured schema management prevents data inconsistencies, ensures scalability, and maintains data integrity across the application lifecycle.

### V. Authentication & Authorization

All protected resources MUST implement proper auth:
- Better Auth MUST be used for user authentication with JWT
- All API endpoints (except auth) MUST require valid JWT token
- User context MUST be extracted from JWT for all operations
- Tasks and user data MUST be scoped to authenticated user
- Passwords MUST NEVER be stored in plaintext
- Secrets and tokens MUST be stored in `.env` files (never committed)

**Rationale**: Security is non-negotiable. Proper auth prevents unauthorized access and ensures user data privacy.

### VI. Frontend Component Standards

Frontend development MUST follow Next.js 14 best practices:
- Use Server Components by default (performance and SEO)
- Client Components MUST be marked with `'use client'` directive (only when interactivity required)
- All API calls MUST go through `/lib/api.ts` client (no direct fetch in components)
- Styling MUST use Tailwind CSS classes (no inline styles)
- Component structure: `/components` for reusable UI, `/app` for pages and layouts
- TypeScript MUST be used for all frontend code (no `any` types)

**Rationale**: Server-first architecture improves performance. Centralized API client ensures consistency. TypeScript prevents runtime errors and improves developer experience.

### VII. Testing & Quality (Conditional)

When tests are explicitly requested in specifications:
- Tests MUST be written FIRST (TDD: Red → Green → Refactor)
- All tests MUST fail before implementation begins
- Contract tests MUST validate API endpoints against specifications
- Integration tests MUST validate user journeys end-to-end
- Unit tests MUST cover business logic and edge cases
- Tests MUST be organized by user story for independent validation

When tests are NOT requested:
- Manual validation MUST be performed against acceptance criteria
- User scenarios from spec MUST be manually tested before completion

**Rationale**: Tests ensure implementation matches specification and prevent regressions. However, rapid prototyping may skip tests initially. Manual validation ensures quality when formal tests are not required.

## Technology Standards

### Frontend Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **State Management**: React hooks (useState, useContext)
- **API Client**: Custom client in `/lib/api.ts`

### Backend Stack
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL
- **Authentication**: Better Auth with JWT
- **Validation**: Pydantic models
- **Python Version**: 3.11+

### Development Environment
- **Package Manager (Frontend)**: npm
- **Package Manager (Backend)**: pip
- **Container Orchestration**: Docker Compose
- **Environment Variables**: `.env` files (not committed)
- **Version Control**: Git with feature branches

## Development Workflow

### Feature Development Lifecycle

1. **Specification Phase** (`/sp.specify`)
   - Write feature spec in `/specs/features/[feature].md`
   - Define user stories with acceptance criteria
   - Identify functional requirements and success metrics
   - Get user approval before proceeding

2. **Planning Phase** (`/sp.plan`)
   - Create implementation plan in `/specs/[feature]/plan.md`
   - Define API contracts in `/specs/api/`
   - Define database schema in `/specs/database/`
   - Define UI components in `/specs/ui/`
   - Validate against constitution principles

3. **Task Generation** (`/sp.tasks`)
   - Generate task list in `/specs/[feature]/tasks.md`
   - Organize tasks by user story priority
   - Mark parallel tasks with `[P]` flag
   - Include test tasks if specified in requirements

4. **Implementation Phase** (`/sp.implement`)
   - Execute tasks in dependency order
   - Backend implementation follows `/backend/CLAUDE.md`
   - Frontend implementation follows `/frontend/CLAUDE.md`
   - Commit after each logical task completion
   - Validate against acceptance criteria

5. **Review & Integration**
   - Manual testing against user scenarios
   - Automated tests if included
   - Code review for spec compliance
   - Update specs if requirements changed during implementation

### Prompt History Records (PHR)

All user interactions MUST be recorded as PHRs:
- **Location**: `history/prompts/`
- **Routing**:
  - Constitution updates → `history/prompts/constitution/`
  - Feature work → `history/prompts/<feature-name>/`
  - General work → `history/prompts/general/`
- **Content**: Full user input (verbatim), concise response summary, metadata (stage, date, files modified)
- **Format**: Use template from `.specify/templates/phr-template.prompt.md`

### Architecture Decision Records (ADR)

Significant architectural decisions MUST be suggested for documentation:
- **Trigger**: Impact (long-term), Alternatives (multiple options), Scope (cross-cutting)
- **Process**: Agent suggests ADR, user approves, then create with `/sp.adr <title>`
- **Location**: `history/adr/`
- **Content**: Context, decision, consequences, alternatives considered

### Commit Standards

All commits MUST follow conventional commit format:
- `feat: add user authentication with Better Auth`
- `fix: resolve task filtering bug in GET /api/tasks`
- `docs: update spec for task-crud feature`
- `refactor: extract API client to /lib/api.ts`
- `test: add integration tests for user stories`

## Governance

### Constitution Authority

This constitution supersedes all other development practices and guidelines. When conflicts arise between this document and other sources:
1. Constitution principles take precedence
2. Spec-Kit conventions follow constitution
3. Framework best practices are adapted to fit constitution
4. Team preferences are subordinate to constitution

### Amendment Process

Constitution amendments require:
1. Clear justification for the change (problem statement)
2. Impact analysis on existing principles and templates
3. Version bump following semantic versioning:
   - **MAJOR**: Backward incompatible changes (principle removal/redefinition)
   - **MINOR**: New principles or material expansions
   - **PATCH**: Clarifications, wording fixes, non-semantic changes
4. Sync propagation to all dependent templates and documentation
5. Migration plan for existing code if necessary

### Compliance Review

All development artifacts MUST pass constitution compliance check:
- Specifications MUST include user scenarios and acceptance criteria
- Plans MUST include constitution check section
- Tasks MUST be organized by user story
- Implementation MUST reference specifications
- PRs MUST validate against constitution principles

### Complexity Justification

When violating simplicity principles (adding abstraction, new dependencies, patterns):
- Violation MUST be documented in plan's Complexity Tracking table
- Justification MUST explain why needed and why simpler alternatives were insufficient
- Approval MUST be obtained before implementation
- Future refactoring to remove complexity MUST be planned

### Runtime Guidance

For agent-specific development guidance during implementation:
- General workflow: `CLAUDE.md` (root)
- Frontend-specific: `frontend/CLAUDE.md`
- Backend-specific: `backend/CLAUDE.md`
- Spec structure: `.spec-kit/config.yaml`
- Templates: `.specify/templates/`

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
