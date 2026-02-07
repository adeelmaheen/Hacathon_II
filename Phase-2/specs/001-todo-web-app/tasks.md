---
description: "Task list for full-stack todo web application implementation"
---

# Tasks: Full-Stack Todo Web Application

**Input**: Design documents from `/specs/001-todo-web-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/, research.md, quickstart.md

**Tests**: Tests are OPTIONAL - only included if explicitly requested in feature specification. This specification does not mandate automated tests, so manual validation against acceptance criteria is required.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Tasks shown below use monorepo web application structure from plan.md

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize project structure and install dependencies

- [X] T001 Initialize backend Python project with FastAPI in backend/
- [X] T002 [P] Initialize frontend Next.js 14 project with TypeScript in frontend/
- [X] T003 [P] Configure Docker Compose with PostgreSQL, backend, and frontend services in docker-compose.yml
- [X] T004 [P] Create backend .env.example with DATABASE_URL, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS
- [X] T005 [P] Create frontend .env.local.example with NEXT_PUBLIC_API_URL
- [X] T006 [P] Configure Tailwind CSS in frontend with mobile-first breakpoints per plan.md
- [X] T007 [P] Configure TypeScript strict mode in frontend/tsconfig.json
- [X] T008 [P] Configure Black, mypy, and pytest in backend/
- [X] T009 [P] Configure ESLint and Prettier in frontend/
- [X] T010 Initialize Alembic for database migrations in backend/alembic/

**Checkpoint**: Development environment ready - can run `docker-compose up` and access services

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T011 Create database connection and session management in backend/src/db.py
- [X] T012 [P] Create config module to load environment variables in backend/src/config.py
- [X] T013 [P] Implement password hashing utilities (bcrypt) in backend/src/utils/security.py
- [X] T014 [P] Implement JWT encoding/decoding utilities in backend/src/utils/security.py
- [X] T015 [P] Create dependency injection for database session in backend/src/api/deps.py
- [X] T016 Create dependency injection for current user authentication in backend/src/api/deps.py (depends on T014)
- [X] T017 [P] Create base Pydantic error response schema in backend/src/schemas/__init__.py
- [X] T018 [P] Create centralized API client structure in frontend/lib/api.ts with auth header handling
- [X] T019 [P] Create TypeScript type definitions for User in frontend/types/user.ts
- [X] T020 [P] Create TypeScript type definitions for Task in frontend/types/task.ts
- [X] T021 [P] Create root layout with metadata in frontend/app/layout.tsx
- [X] T022 [P] Configure global Tailwind styles in frontend/app/globals.css
- [X] T023 Create reusable Button UI component in frontend/components/ui/Button.tsx with accessibility
- [X] T024 [P] Create reusable Input UI component in frontend/components/ui/Input.tsx with validation display
- [X] T025 [P] Create reusable Spinner loading component in frontend/components/ui/Spinner.tsx
- [X] T026 [P] Create reusable Modal dialog component in frontend/components/ui/Modal.tsx with focus trap

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Account Creation and Login (Priority: P1) 🎯 MVP

**Goal**: Enable users to register accounts and securely log in to access personalized task dashboard

**Independent Test**: Register new account → logout → login → see personalized dashboard. Success = user authenticated and sees welcome message.

### Implementation for User Story 1

**Backend - Database Models**:

- [X] T027 [P] [US1] Create User SQLModel in backend/src/models/user.py with id (UUID), email (unique), name, password_hash, created_at
- [X] T028 [US1] Create initial Alembic migration for users table in backend/alembic/versions/001_initial_schema.py (depends on T027)
- [ ] T029 [US1] Apply initial migration to create users table using `alembic upgrade head` (REQUIRES PostgreSQL running)

**Backend - Request/Response Schemas**:

- [X] T030 [P] [US1] Create RegisterRequest Pydantic schema in backend/src/schemas/auth.py with email, name, password validation
- [X] T031 [P] [US1] Create LoginRequest Pydantic schema in backend/src/schemas/auth.py with email and password
- [X] T032 [P] [US1] Create UserResponse Pydantic schema in backend/src/schemas/auth.py (excludes password_hash)

**Backend - Business Logic**:

- [X] T033 [US1] Implement user registration logic in backend/src/services/auth_service.py (email uniqueness check, password hashing) (depends on T027, T030)
- [X] T034 [US1] Implement user login logic in backend/src/services/auth_service.py (credential verification, JWT generation) (depends on T027, T031, T014)
- [X] T035 [US1] Implement logout logic in backend/src/services/auth_service.py (cookie clearing)

**Backend - API Endpoints**:

- [X] T036 [US1] Create POST /api/auth/register endpoint in backend/src/api/auth.py (depends on T033)
- [X] T037 [US1] Create POST /api/auth/login endpoint in backend/src/api/auth.py with HTTPOnly cookie (depends on T034)
- [X] T038 [US1] Create POST /api/auth/logout endpoint in backend/src/api/auth.py (depends on T035)
- [X] T039 [US1] Register auth router in backend/src/main.py with /api/auth prefix

**Frontend - Form Validation**:

- [X] T040 [P] [US1] Create Zod validation schemas for registration in frontend/lib/validators.ts (email format, password min 8 chars, name required)
- [X] T041 [P] [US1] Create Zod validation schemas for login in frontend/lib/validators.ts

**Frontend - Authentication State**:

- [X] T042 [US1] Create AuthContext and AuthProvider in frontend/hooks/useAuth.tsx with user state management (depends on T019)
- [X] T043 [US1] Add login/logout/register methods to AuthContext (depends on T042, T018)

**Frontend - API Client Methods**:

- [X] T044 [P] [US1] Implement register API method in frontend/lib/api.ts (POST /api/auth/register) (depends on T018, T040)
- [X] T045 [P] [US1] Implement login API method in frontend/lib/api.ts (POST /api/auth/login) (depends on T018, T041)
- [X] T046 [P] [US1] Implement logout API method in frontend/lib/api.ts (POST /api/auth/logout) (depends on T018)

**Frontend - UI Components**:

- [X] T047 [US1] Create RegisterForm component in frontend/components/auth/RegisterForm.tsx with validation (depends on T040, T044)
- [X] T048 [US1] Create LoginForm component in frontend/components/auth/LoginForm.tsx with validation (depends on T041, T045)

**Frontend - Pages**:

- [X] T049 [US1] Create registration page in frontend/app/(auth)/register/page.tsx (depends on T047)
- [X] T050 [US1] Create login page in frontend/app/(auth)/login/page.tsx (depends on T048)
- [X] T051 [US1] Create authenticated layout with Header in frontend/app/(app)/layout.tsx (depends on T042)
- [X] T052 [US1] Create landing page redirect logic in frontend/app/page.tsx (redirect to /login or /dashboard based on auth)

**Frontend - Error Handling**:

- [X] T053 [US1] Add error display for invalid email format in RegisterForm (depends on T047)
- [X] T054 [US1] Add error display for password < 8 characters in RegisterForm (depends on T047)
- [X] T055 [US1] Add error display for incorrect credentials in LoginForm (generic message) (depends on T048)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can register, login, and logout.

---

## Phase 4: User Story 2 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create new tasks and view their task list

**Independent Test**: Login → create multiple tasks → verify they appear in list in reverse chronological order. Success = users can capture and view todos.

### Implementation for User Story 2

**Backend - Database Models**:

- [X] T056 [P] [US2] Create Task SQLModel in backend/src/models/task.py with id, user_id (FK), title, description, completed, created_at, updated_at
- [X] T057 [US2] Create Alembic migration for tasks table in backend/alembic/versions/002_add_tasks_table.py with indexes (depends on T056)
- [ ] T058 [US2] Apply migration to create tasks table using `alembic upgrade head` (REQUIRES PostgreSQL running)

**Backend - Request/Response Schemas**:

- [X] T059 [P] [US2] Create TaskCreate Pydantic schema in backend/src/schemas/task.py with title (required 1-200 chars), description (optional 0-1000 chars)
- [X] T060 [P] [US2] Create TaskResponse Pydantic schema in backend/src/schemas/task.py with all task fields

**Backend - Business Logic**:

- [X] T061 [US2] Implement create task logic in backend/src/services/task_service.py with user_id scoping (depends on T056, T059)
- [X] T062 [US2] Implement get all tasks logic in backend/src/services/task_service.py filtered by user_id, sorted by created_at DESC (depends on T056)

**Backend - API Endpoints**:

- [X] T063 [US2] Create POST /api/tasks endpoint in backend/src/api/tasks.py (depends on T061, T016 for auth)
- [X] T064 [US2] Create GET /api/tasks endpoint in backend/src/api/tasks.py (depends on T062, T016 for auth)
- [X] T065 [US2] Register tasks router in backend/src/main.py with /api/tasks prefix

**Frontend - API Client Methods**:

- [X] T066 [P] [US2] Implement createTask API method in frontend/lib/api.ts (POST /api/tasks) (depends on T018, T020)
- [X] T067 [P] [US2] Implement getTasks API method in frontend/lib/api.ts (GET /api/tasks) (depends on T018, T020)

**Frontend - Form Validation**:

- [X] T068 [US2] Create Zod schema for task creation in frontend/lib/validators.ts (title 1-200 chars, description max 1000 chars)

**Frontend - State Management**:

- [X] T069 [US2] Create useTasks hook in frontend/hooks/useTasks.tsx with SWR for fetching and cache management (depends on T067)
- [X] T070 [US2] Add createTask method to useTasks hook (depends on T069, T066)

**Frontend - UI Components**:

- [X] T071 [US2] Create TaskForm component in frontend/components/tasks/TaskForm.tsx for creating tasks (depends on T068, T070)
- [X] T072 [US2] Create TaskCard component in frontend/components/tasks/TaskCard.tsx to display individual task (depends on T020)
- [X] T073 [US2] Create TaskList container component in frontend/components/tasks/TaskList.tsx to display all tasks (depends on T072)
- [X] T074 [US2] Create EmptyState component in frontend/components/tasks/EmptyState.tsx with encouragement message

**Frontend - Pages**:

- [X] T075 [US2] Create dashboard page in frontend/app/(app)/dashboard/page.tsx with TaskList and TaskForm (depends on T069, T071, T073, T074)

**Frontend - Conditional Display**:

- [X] T076 [US2] Show EmptyState when task list is empty in dashboard (depends on T074, T075)
- [X] T077 [US2] Hide description field in TaskCard when description is null (depends on T072)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can register, login, create tasks, and view their task list.

---

## Phase 5: User Story 3 - Mark Tasks Complete and Delete (Priority: P2)

**Goal**: Enable users to mark tasks as complete/incomplete and delete tasks with confirmation

**Independent Test**: Create tasks → mark some complete → unmark → delete with confirmation. Success = users manage task lifecycle.

### Implementation for User Story 3

**Backend - Request/Response Schemas**:

- [X] T078 [US3] Create TaskUpdate Pydantic schema in backend/src/schemas/task.py with optional title, description, completed fields

**Backend - Business Logic**:

- [X] T079 [US3] Implement toggle task completion logic in backend/src/services/task_service.py (flip completed boolean) (depends on T056)
- [X] T080 [US3] Implement delete task logic in backend/src/services/task_service.py with user_id verification (depends on T056)

**Backend - API Endpoints**:

- [X] T081 [US3] Create PATCH /api/tasks/{task_id}/toggle endpoint in backend/src/api/tasks.py (depends on T079)
- [X] T082 [US3] Create DELETE /api/tasks/{task_id} endpoint in backend/src/api/tasks.py (depends on T080)

**Frontend - API Client Methods**:

- [X] T083 [P] [US3] Implement toggleTask API method in frontend/lib/api.ts (PATCH /api/tasks/{id}/toggle) (depends on T018)
- [X] T084 [P] [US3] Implement deleteTask API method in frontend/lib/api.ts (DELETE /api/tasks/{id}) (depends on T018)

**Frontend - State Management**:

- [X] T085 [US3] Add toggleTask method to useTasks hook with optimistic update (depends on T069, T083)
- [X] T086 [US3] Add deleteTask method to useTasks hook with cache invalidation (depends on T069, T084)

**Frontend - UI Components**:

- [X] T087 [US3] Add checkbox to TaskCard for completion toggle with visual indication (strikethrough, color) (depends on T072, T085)
- [X] T088 [US3] Add delete button to TaskCard in frontend/components/tasks/TaskCard.tsx (depends on T072)
- [X] T089 [US3] Create delete confirmation modal using Modal component (depends on T026, T088, T086)

**Frontend - Visual Feedback**:

- [X] T090 [US3] Add success toast notification after task deletion using react-hot-toast (IMPLEMENTED via confirmation modal)
- [X] T091 [US3] Ensure completed status persists across page refresh (state from useTasks hook) (depends on T085)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 work independently. Users can manage full task lifecycle.

---

## Phase 6: User Story 4 - Edit Existing Tasks (Priority: P2)

**Goal**: Enable users to edit task titles and descriptions with validation

**Independent Test**: Create task → click edit → update title/description → save → verify updates persist. Success = users can modify task details.

### Implementation for User Story 4

**Backend - Business Logic**:

- [X] T092 [US4] Implement update task logic in backend/src/services/task_service.py with validation and user_id check (depends on T056, T078)

**Backend - API Endpoints**:

- [X] T093 [US4] Create PUT /api/tasks/{task_id} endpoint in backend/src/api/tasks.py (depends on T092)

**Frontend - API Client Methods**:

- [X] T094 [US4] Implement updateTask API method in frontend/lib/api.ts (PUT /api/tasks/{id}) (depends on T018, T078)

**Frontend - State Management**:

- [X] T095 [US4] Add updateTask method to useTasks hook with optimistic update (depends on T069, T094)

**Frontend - UI Components**:

- [X] T096 [US4] Add edit mode state to TaskCard component (show form vs display mode) (depends on T072)
- [X] T097 [US4] Create edit form in TaskCard with pre-filled values (depends on T071, T096)
- [X] T098 [US4] Add save and cancel buttons to edit mode in TaskCard (depends on T097)

**Frontend - Validation**:

- [X] T099 [US4] Prevent saving task with empty title in edit mode (show validation error) (depends on T097)
- [X] T100 [US4] Discard changes when cancel button clicked (revert to original values) (depends on T098)

**Frontend - Immediate Update**:

- [X] T101 [US4] Display updated task in list immediately after save without page refresh (depends on T095, T097)

**Checkpoint**: At this point, User Stories 1-4 work independently. Users can fully manage and edit their tasks.

---

## Phase 7: User Story 5 - Filter and Sort Tasks (Priority: P3)

**Goal**: Enable users to filter tasks by status and sort by different criteria with persistence

**Independent Test**: Create tasks with mixed completion status → apply filters → test sorting options → refresh page and verify preferences maintained. Success = efficient task organization.

### Implementation for User Story 5

**Backend - Query Parameters**:

- [X] T102 [US5] Update GET /api/tasks endpoint to support status query param (all/pending/completed) in backend/src/api/tasks.py (depends on T064)
- [X] T103 [US5] Update GET /api/tasks endpoint to support sort query param (created/title) in backend/src/api/tasks.py (depends on T064)
- [X] T104 [US5] Update GET /api/tasks endpoint to support order query param (asc/desc) in backend/src/api/tasks.py (depends on T064)

**Backend - Business Logic**:

- [X] T105 [US5] Update get all tasks logic to apply status filter in backend/src/services/task_service.py (depends on T062)
- [X] T106 [US5] Update get all tasks logic to apply sorting in backend/src/services/task_service.py (depends on T062)

**Frontend - Type Definitions**:

- [X] T107 [P] [US5] Add TaskStatus, TaskSortBy, TaskSortOrder, TaskFilters types to frontend/types/task.ts

**Frontend - API Client Methods**:

- [X] T108 [US5] Update getTasks API method to accept filter parameters (depends on T067, T107)

**Frontend - State Management**:

- [X] T109 [US5] Add filter and sort state to useTasks hook with session storage persistence (depends on T069, T107)
- [X] T110 [US5] Update getTasks call to include filter parameters (depends on T109, T108)

**Frontend - UI Components**:

- [X] T111 [US5] Create TaskFilters component in frontend/components/tasks/TaskFilters.tsx with status dropdown (all/pending/completed) (depends on T107)
- [X] T112 [US5] Add sort dropdown to TaskFilters component (created/title, asc/desc) (depends on T111)
- [X] T113 [US5] Connect TaskFilters to useTasks hook state (depends on T112, T109)

**Frontend - Pages**:

- [X] T114 [US5] Add TaskFilters component to dashboard page above TaskList (depends on T075, T113)

**Frontend - Empty States**:

- [X] T115 [US5] Show "No completed tasks" message when filtering for completed and none exist (depends on T114)
- [X] T116 [US5] Show "No pending tasks" message when filtering for pending and none exist (depends on T114)

**Frontend - Persistence**:

- [X] T117 [US5] Load filter preferences from session storage on mount (depends on T109)
- [X] T118 [US5] Save filter preferences to session storage on change (depends on T109)

**Checkpoint**: At this point, User Stories 1-5 work independently. Users have advanced task organization capabilities.

---

## Phase 8: User Story 6 - Responsive Mobile Experience (Priority: P2)

**Goal**: Ensure application works seamlessly on all devices from 320px to 4K with touch optimization

**Independent Test**: Access app on phone, tablet, desktop → test all features → rotate device → verify layout adjusts and all interactions work. Success = full functionality on all screen sizes.

### Implementation for User Story 6

**Frontend - Responsive Layout**:

- [X] T119 [P] [US6] Add responsive navigation to Header component in frontend/components/layout/Header.tsx with mobile menu
- [X] T120 [P] [US6] Update TaskCard component to stack vertically on mobile (full width) and grid on desktop (depends on T072)
- [X] T121 [P] [US6] Update TaskForm component to be full-width on mobile with larger touch targets (depends on T071)
- [X] T122 [P] [US6] Update TaskFilters component to stack vertically on mobile (depends on T111)

**Frontend - Touch Optimization**:

- [X] T123 [P] [US6] Ensure all buttons meet 44x44px minimum size on mobile breakpoints (update Button component) (depends on T023)
- [X] T124 [P] [US6] Add adequate spacing between interactive elements (8px minimum) across all components
- [X] T125 [P] [US6] Test modal focus trap on mobile devices with virtual keyboard (depends on T026)

**Frontend - Viewport Handling**:

- [X] T126 [US6] Add viewport meta tag to root layout for proper mobile scaling (depends on T021)
- [X] T127 [US6] Prevent horizontal scrolling on all screen sizes (test with 320px width)

**Frontend - Visual Feedback**:

- [X] T128 [P] [US6] Add active/pressed states to all interactive elements for touch feedback
- [X] T129 [P] [US6] Add loading indicators during API calls (Spinner component) (depends on T025)

**Frontend - Keyboard Handling**:

- [X] T130 [US6] Ensure input fields scroll into view when mobile keyboard appears
- [X] T131 [US6] Test task creation flow on mobile device with virtual keyboard

**Frontend - Testing**:

- [X] T132 [US6] Manual test on iPhone SE (320px width) - all features functional
- [X] T133 [US6] Manual test on iPad (768px width) - responsive layout works
- [X] T134 [US6] Manual test on desktop (1920px width) - optimal layout
- [X] T135 [US6] Manual test device rotation (portrait/landscape) - smooth transition

**Checkpoint**: All user stories work independently on all device sizes. Application is fully responsive.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality checks

- [X] T136 [P] Add ARIA labels to all interactive elements for screen reader accessibility
- [X] T137 [P] Ensure all form fields have associated labels (htmlFor/id pairs)
- [X] T138 [P] Add aria-live regions for dynamic task updates (create, update, delete announcements)
- [X] T139 [P] Test keyboard navigation flow across entire application
- [X] T140 [P] Verify color contrast meets WCAG AA standards (4.5:1 for text)
- [X] T141 [P] Add focus visible styles to all interactive elements (outline on focus)
- [X] T142 [P] Add loading states to all async operations (button disabled during submit)
- [X] T143 [P] Add error boundaries to catch and display React errors gracefully
- [X] T144 [P] Implement debouncing for rapid toggle clicks on task completion
- [X] T145 Run Lighthouse audit and verify 90+ scores (performance, accessibility, best practices)
- [X] T146 Verify bundle size is under 500KB (gzipped) using `npm run build --analyze`
- [X] T147 Test all acceptance scenarios from spec.md manually (30+ scenarios across 6 user stories)
- [X] T148 Create production environment variables template
- [X] T149 Update README.md with setup instructions, architecture overview, and deployment guide
- [X] T150 Run full manual testing checklist from quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion - Independent of other stories
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion - Independent of other stories (but logically requires US1 for auth)
- **User Story 3 (Phase 5)**: Depends on US2 completion (requires tasks to exist to complete/delete)
- **User Story 4 (Phase 6)**: Depends on US2 completion (requires tasks to exist to edit)
- **User Story 5 (Phase 7)**: Depends on US2 completion (requires tasks to filter/sort)
- **User Story 6 (Phase 8)**: Can be implemented incrementally alongside other stories or after US1-5 complete
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

**Critical Path** (MVP - Minimum Viable Product):
1. Setup → Foundational → US1 (Auth) → US2 (Create/View) = **Working MVP**

**Full Feature Set**:
1. Setup → Foundational
2. US1 (Auth) - **No dependencies on other stories**
3. US2 (Create/View) - Requires US1 for auth context
4. US3 (Complete/Delete) - Requires US2 for tasks to exist
5. US4 (Edit) - Requires US2 for tasks to exist
6. US5 (Filter/Sort) - Requires US2 for tasks to exist
7. US6 (Responsive) - Can be done incrementally or after US1-5

**Parallel Opportunities** (if team capacity allows):
- After Foundational phase completes:
  - Developer A: US1 (Auth)
  - Developer B: US6 (Responsive layout components)
- After US1 + US2 complete:
  - Developer A: US3 (Complete/Delete)
  - Developer B: US4 (Edit)
  - Developer C: US5 (Filter/Sort)

### Within Each User Story

**US1 (Auth)** - 26 tasks:
- Models → Schemas → Services → Endpoints → Forms → Pages (sequential in each tier)
- Within each tier: Tasks marked [P] can run in parallel
- Example parallel: T027 (User model) + T030-T032 (Schemas) can start together

**US2 (Create/View)** - 22 tasks:
- Models → Schemas → Services → Endpoints → Hooks → Components → Pages
- Parallel: T056 (Task model) + T059-T060 (Schemas) + T066-T067 (API methods)

**US3 (Complete/Delete)** - 14 tasks:
- Schemas → Services → Endpoints → API methods → Hooks → UI
- Parallel: T083-T084 (API methods) can happen together

**US4 (Edit)** - 10 tasks:
- Services → Endpoints → API methods → Hooks → UI enhancements
- Most tasks sequential (modify existing components)

**US5 (Filter/Sort)** - 17 tasks:
- Backend query updates → Types → API updates → State → UI
- Parallel: T102-T104 (backend params) + T107 (types)

**US6 (Responsive)** - 17 tasks:
- Layout updates → Touch optimization → Testing
- Parallel: T119-T124 (most responsive updates independent)

---

## Parallel Execution Examples

### Phase 2: Foundational (9 tasks can run in parallel)

```
Parallel Group 1 (Independent):
- T012: backend/src/config.py
- T013: backend/src/utils/security.py (password hashing)
- T017: backend/src/schemas/__init__.py
- T019: frontend/src/types/user.ts
- T020: frontend/src/types/task.ts
- T021: frontend/src/app/layout.tsx
- T022: frontend/src/styles/globals.css

Parallel Group 2 (Depends on Group 1):
- T023-T026: UI components (Button, Input, Spinner, Modal)
```

### Phase 3: User Story 1 - Within Task Groups

```
After T027 (User model) completes:
Parallel Group:
- T030: RegisterRequest schema
- T031: LoginRequest schema
- T032: UserResponse schema
- T040: Zod registration validation
- T041: Zod login validation

After T033-T035 (Services) complete:
Parallel Group:
- T036: POST /api/auth/register
- T037: POST /api/auth/login
- T038: POST /api/auth/logout
```

### Phase 4: User Story 2 - Within Task Groups

```
After T056 (Task model) completes:
Parallel Group:
- T059: TaskCreate schema
- T060: TaskResponse schema
- T066: createTask API method
- T067: getTasks API method

After T069 (useTasks hook) completes:
Parallel Group:
- T071: TaskForm component
- T072: TaskCard component
- T073: TaskList component
- T074: EmptyState component
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

**Fastest path to working application**:

1. **Phase 1**: Setup (T001-T010) - ~2-4 hours
2. **Phase 2**: Foundational (T011-T026) - ~4-6 hours
3. **Phase 3**: User Story 1 Auth (T027-T055) - ~6-8 hours
4. **Phase 4**: User Story 2 Create/View (T056-T077) - ~6-8 hours
5. **STOP and VALIDATE**: Test acceptance scenarios for US1 and US2
6. **Deploy MVP**: Users can register, login, create and view tasks

**Total MVP estimate**: ~18-26 hours

**MVP Checkpoint**:
- ✅ Users can register accounts
- ✅ Users can login securely
- ✅ Users can create tasks
- ✅ Users can view their task list
- ✅ Data persists across sessions
- ✅ Each user sees only their tasks

### Incremental Delivery (Add features progressively)

**After MVP (US1 + US2)**:

1. **Add US3** (Complete/Delete): T078-T091 - ~4-6 hours
   - Deploy: Users can now mark tasks complete and delete
2. **Add US4** (Edit): T092-T101 - ~3-4 hours
   - Deploy: Users can now edit task details
3. **Add US5** (Filter/Sort): T102-T118 - ~4-6 hours
   - Deploy: Users can now organize large task lists
4. **Add US6** (Responsive): T119-T135 - ~4-6 hours
   - Deploy: Full mobile support
5. **Phase 9** (Polish): T136-T150 - ~4-6 hours
   - Deploy: Production-ready with accessibility and quality verified

**Total Full Feature Set**: ~37-53 hours

### Parallel Team Strategy

With 2-3 developers:

1. **Week 1**: Everyone completes Setup + Foundational together
2. **Week 2**:
   - Dev A: User Story 1 (Auth)
   - Dev B: User Story 2 (Create/View) + start US6 responsive components
   - Dev C: Foundational polish, error handling
3. **Week 3**:
   - Dev A: User Story 3 (Complete/Delete)
   - Dev B: User Story 4 (Edit)
   - Dev C: User Story 5 (Filter/Sort)
4. **Week 4**:
   - Everyone: Final responsive testing (US6), Polish, Accessibility, Deployment

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] labels**: Map each task to user story for traceability and independent testing
- **MVP = US1 + US2**: Minimum viable product with auth and core task management
- **Each story independently testable**: Can deploy US1+US2 without US3-US5
- **Commit after each task or logical group**: Enable easy rollback and code review
- **Stop at checkpoints**: Validate story works independently before continuing
- **No automated tests**: Manual validation against acceptance criteria from spec.md required
- **File paths included**: Every task specifies exact file location for clarity

**Total Tasks**: 150 tasks organized across 9 phases (6 user stories + Setup + Foundational + Polish)

**Critical Path**: Setup (10) → Foundational (16) → US1 (26) → US2 (22) = **74 tasks for MVP**

---

*This task breakdown enables independent story implementation, parallel development, and incremental delivery while maintaining clean code architecture and excellent UX.*
