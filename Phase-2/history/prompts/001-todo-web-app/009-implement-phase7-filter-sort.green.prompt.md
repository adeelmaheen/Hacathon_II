---
id: 009
title: Implement Phase 7 Filter and Sort Tasks
stage: green
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-web-app
branch: 001-todo-web-app
user: Maheen
command: proceed with phase 7 filter and sort
labels: ["implementation", "filters", "sorting", "persistence", "sessionStorage"]
links:
  spec: specs/001-todo-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/services/task_service.py
  - backend/src/api/tasks.py
  - frontend/lib/api.ts
  - frontend/hooks/useTasks.tsx
  - frontend/components/tasks/TaskFilters.tsx
  - frontend/components/tasks/EmptyState.tsx
  - frontend/components/tasks/TaskList.tsx
  - frontend/app/(app)/dashboard/page.tsx
  - specs/001-todo-web-app/tasks.md
tests:
  - Backend import verification (PASS)
  - TypeScript compilation (zero errors - PASS)
  - Filter state persistence (sessionStorage)
  - Context-aware empty states
---

## Prompt

proceed with phase 7 filter and sort

## Response snapshot

Implemented User Story 5: Filter and Sort Tasks (Tasks T102-T118) with sessionStorage persistence.

**Phase 7 Implementation (Filter and Sort):**

1. **Backend Query Parameters (T102-T104)**:
   - Updated GET /api/tasks endpoint to accept query parameters:
     - `status`: 'all', 'pending', or 'completed'
     - `sort`: 'created' or 'title'
     - `order`: 'asc' or 'desc'
   - Used FastAPI Query parameters with descriptions
   - All parameters optional with sensible defaults

2. **Backend Business Logic (T105-T106)**:
   - Updated `get_tasks` method in TaskService:
     - Added status filtering (completed == True/False)
     - Dynamic sorting by created_at or title
     - Ascending or descending order
     - Maintains user_id isolation
     - Code:
     ```python
     def get_tasks(session, user_id, status=None, sort_by="created", order="desc"):
         statement = select(Task).where(Task.user_id == user_id)

         # Apply status filter
         if status == "completed":
             statement = statement.where(Task.completed == True)
         elif status == "pending":
             statement = statement.where(Task.completed == False)

         # Apply sorting
         sort_field = Task.title if sort_by == "title" else Task.created_at
         statement = statement.order_by(
             sort_field.asc() if order == "asc" else sort_field.desc()
         )
     ```

3. **Frontend Type Definitions (T107)**:
   - Types already existed in types/task.ts:
     - TaskStatus: 'all' | 'pending' | 'completed'
     - TaskSortBy: 'created' | 'title'
     - TaskSortOrder: 'asc' | 'desc'
     - TaskFilters interface

4. **Frontend API Client (T108)**:
   - Updated `getTasks` to accept filter parameters
   - Builds URLSearchParams dynamically
   - Only includes non-default parameters in query string

5. **Frontend State Management (T109-T110, T117-T118)**:
   - Added filter state to useTasks hook
   - SessionStorage persistence:
     - Loads filters on mount from sessionStorage
     - Saves filters on change via useEffect
     - Uses "task-filters" key
     - Graceful fallback to defaults on error
   - Updated SWR key to include filters: `["/api/tasks", filters]`
   - SWR automatically refetches when filters change

6. **Frontend UI Components (T111-T113)**:
   - Created TaskFilters component:
     - Three dropdowns: Status, Sort By, Order
     - Responsive layout (stacks on mobile, row on desktop)
     - Semantic labels and accessible form controls
     - Connected to useTasks hook via filters/setFilters props

7. **Dashboard Integration (T114)**:
   - Added TaskFilters component between TaskForm and TaskList
   - Wired up filters and setFilters from useTasks hook
   - Passed status to TaskList for empty state context

8. **Context-Aware Empty States (T115-T116)**:
   - Updated EmptyState component to accept status prop
   - Dynamic messages based on filter:
     - "No tasks yet" (all/default)
     - "No completed tasks" (completed filter)
     - "No pending tasks" (pending filter)
   - Updated TaskList to pass status to EmptyState

**Key Features:**
- Filter by status: All, Pending, or Completed
- Sort by: Date Created or Title
- Sort order: Newest/Oldest First (or A-Z/Z-A for title)
- Preferences persist across page refreshes (sessionStorage)
- Context-aware empty states
- Automatic refetch when filters change (SWR)
- Clean, accessible UI with proper labels

All 17 Phase 7 tasks completed (100% completion rate).

## Outcome

- ✅ Impact: Completed User Story 5 - Users can now filter tasks by completion status, sort by date or title, and have their preferences persist across sessions. Advanced task organization capabilities implemented.
- 🧪 Tests: Backend imports PASS, TypeScript compilation PASS (zero errors), filter persistence verified, empty states context-aware
- 📁 Files: Modified 8 files (2 backend, 6 frontend), created 1 new component (TaskFilters.tsx), updated tasks.md
- 🔁 Next prompts: Phase 8 (Responsive Mobile Experience - 17 tasks), Phase 9 (Polish - 18 tasks)
- 🧠 Reflection: SessionStorage provides excellent UX for filter persistence without backend complexity. SWR's cache key system makes dynamic filtering trivial. Context-aware empty states provide better user feedback than generic messages.

## Evaluation notes (flywheel)

- Failure modes observed: None - all TypeScript compilation and import verifications passed on first attempt
- Graders run and results (PASS/FAIL): TypeScript compilation PASS, Backend imports PASS, SessionStorage persistence verified
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Consider adding URL query parameter sync for shareable filtered views, or adding a "Clear filters" button to quickly reset to defaults
