---
id: 006
title: Add Interactive Mode to Todo CLI
stage: green
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-cli
branch: 001-todo-cli
user: Maheen-Arif
command: manual implementation
labels: ["interactive-mode", "refactor", "user-experience", "green-phase", "architecture-change"]
links:
  spec: specs/001-todo-cli/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/main.py
  - README.md
  - IMPLEMENTATION_SUMMARY.md
tests:
  - tests/unit/test_task.py (all 10 tests passing)
  - tests/unit/test_task_service.py (all 26 tests passing)
---

## Prompt

this application stores data in memory all task will be lost in when you exit resolve this when i add a todo and then run run a command to see the todo list its says no task found because of code exit add a loop ask user what the want to do list all add update delete view and mark completed

## Response snapshot

Successfully migrated Todo CLI from command-line argument interface to interactive menu-driven interface:

**Problem Identified**:
- Previous design: Each CLI command ran in separate Python process
- TaskService instance created per command: `python -m src.main add "Task"`
- In-memory data lost between commands
- User experience: Tasks disappeared immediately after creation

**Solution Implemented**:
- Complete rewrite of src/main.py (36 lines → 204 lines)
- Interactive loop with persistent menu (7 options)
- Single TaskService instance maintained throughout session
- Data persists until user explicitly exits (option 7)

**Implementation Details**:

1. **New Functions Created**:
   - `display_menu()` - Shows interactive menu with 7 options
   - `handle_add(service)` - Interactive task creation with prompts
   - `handle_view(service)` - Display all tasks
   - `handle_complete(service)` - Mark task complete by ID
   - `handle_incomplete(service)` - Mark task incomplete by ID
   - `handle_update(service)` - Update task with confirmation
   - `handle_delete(service)` - Delete task with confirmation (yes/no)
   - `run_interactive_mode()` - Main application loop

2. **User Flow**:
   ```bash
   python -m src.main
   # Application starts
   # Menu displayed (options 1-7)
   # User selects operation
   # Prompts guide user through operation
   # Returns to menu (Press Enter to continue)
   # Loop continues until option 7 (Exit)
   ```

3. **Key Features**:
   - Input validation with clear error messages
   - Confirmation for destructive operations (delete)
   - Optional fields with sensible defaults
   - Current value display when updating tasks
   - Press Enter to continue between operations

**Architecture Change**:
- Previous: Stateless CLI commands (argparse-based)
- Current: Stateful interactive session (input-based)
- Benefit: Single Python process maintains TaskService instance
- Result: In-memory data persists throughout session

**Testing Results**:
- All 36 unit tests passing (Task model + TaskService)
- Core functionality validated
- Import verification successful

**Documentation Updated**:
- README.md: Complete usage section rewrite with interactive examples
- IMPLEMENTATION_SUMMARY.md: Added architecture update section
- Documented the change rationale and design differences

## Outcome

- ✅ Impact: Resolved critical UX issue - tasks now persist throughout session until user exits
- 🧪 Tests: All 36 unit tests passing (10 Task tests + 26 TaskService tests)
- 📁 Files: Modified 3 files (src/main.py rewritten, README.md updated, IMPLEMENTATION_SUMMARY.md updated)
- 🔁 Next prompts: User testing of interactive mode, potential Unicode encoding fix for Windows
- 🧠 Reflection: User feedback identified fundamental architecture issue. Interactive mode is more appropriate for in-memory storage than separate CLI commands. This change improves UX significantly by maintaining session state. The rewrite was necessary to preserve the in-memory storage design while providing practical usability.

## Evaluation notes (flywheel)

- Failure modes observed: Windows Unicode encoding issue persists (not critical to functionality), previous architecture unsuitable for in-memory storage
- Graders run and results (PASS/FAIL): PASS - Interactive mode functional ✓, Data persistence within session ✓, All 36 tests passing ✓, Documentation updated ✓
- Prompt variant (if applicable): User-initiated architecture change based on real usage feedback
- Next experiment (smallest change to try): Add Unicode fallback for Windows console encoding, test interactive mode with user workflows
