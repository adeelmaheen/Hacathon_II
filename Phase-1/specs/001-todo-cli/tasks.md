---

description: "Task list for Todo CLI Application implementation"
---

# Tasks: Todo CLI Application

**Input**: Design documents from `/specs/001-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD is MANDATORY per constitution. All tests must be written before implementation (Red-Green-Refactor).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create src directory structure (src/, src/models/, src/services/, src/cli/)
- [X] T002 Create tests directory structure (tests/, tests/unit/, tests/integration/)
- [X] T003 [P] Create all __init__.py files in src/ and subdirectories
- [X] T004 [P] Create all __init__.py files in tests/ and subdirectories
- [X] T005 Create pyproject.toml with UV configuration and dev dependencies
- [X] T006 Create .gitignore with Python patterns
- [X] T007 [P] Install development dependencies with UV (pytest, pytest-cov, ruff)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 [P] Create custom exception classes in src/models/exceptions.py (TaskNotFoundError, ValidationError)
- [X] T009 Write unit tests for Task model validation in tests/unit/test_task.py (TDD: RED)
- [X] T010 Implement Task model with validation in src/models/task.py (TDD: GREEN)
- [X] T011 Refactor Task model if needed (TDD: REFACTOR)
- [X] T012 Write unit tests for TaskService initialization in tests/unit/test_task_service.py (TDD: RED)
- [X] T013 Implement TaskService __init__ method in src/services/task_service.py (TDD: GREEN)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title and description, tasks get unique IDs

**Independent Test**: Run add command, verify task appears in list with correct title, description, incomplete status

### Tests for User Story 1 (TDD: RED)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Write unit tests for TaskService.add() method in tests/unit/test_task_service.py
- [ ] T015 [P] [US1] Write unit tests for add command validation in tests/unit/test_commands.py
- [ ] T016 [P] [US1] Write integration test for add command CLI in tests/integration/test_cli_add.py

### Implementation for User Story 1 (TDD: GREEN)

- [ ] T017 [US1] Implement TaskService.add() method in src/services/task_service.py
- [ ] T018 [US1] Implement add command argparse setup in src/cli/commands.py
- [ ] T019 [US1] Implement add command handler in src/cli/commands.py
- [ ] T020 [US1] Add error handling for validation errors in add command

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can view all tasks with status indicators (✓/○)

**Independent Test**: Add tasks, view list, verify all tasks displayed with correct status indicators

### Tests for User Story 2 (TDD: RED)

- [ ] T021 [P] [US2] Write unit tests for TaskService.list_all() method in tests/unit/test_task_service.py
- [ ] T022 [P] [US2] Write unit tests for formatter status indicators in tests/unit/test_formatter.py
- [ ] T023 [P] [US2] Write unit tests for list command in tests/unit/test_commands.py
- [ ] T024 [P] [US2] Write integration test for list command CLI in tests/integration/test_cli_list.py

### Implementation for User Story 2 (TDD: GREEN)

- [ ] T025 [US2] Implement TaskService.list_all() method in src/services/task_service.py
- [ ] T026 [P] [US2] Implement status_indicator() function in src/cli/formatter.py
- [ ] T027 [P] [US2] Implement format_task_list() function in src/cli/formatter.py
- [ ] T028 [US2] Implement list command argparse setup in src/cli/commands.py
- [ ] T029 [US2] Implement list command handler in src/cli/commands.py
- [ ] T030 [US2] Handle empty task list display ("No tasks found")

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (MVP complete!)

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion status

**Independent Test**: Add task, mark complete (verify ✓), mark incomplete (verify ○), view list to confirm

### Tests for User Story 3 (TDD: RED)

- [ ] T031 [P] [US3] Write unit tests for TaskService.complete() method in tests/unit/test_task_service.py
- [ ] T032 [P] [US3] Write unit tests for TaskService.uncomplete() method in tests/unit/test_task_service.py
- [ ] T033 [P] [US3] Write unit tests for TaskService.get() method in tests/unit/test_task_service.py
- [ ] T034 [P] [US3] Write unit tests for complete command in tests/unit/test_commands.py
- [ ] T035 [P] [US3] Write unit tests for incomplete command in tests/unit/test_commands.py
- [ ] T036 [P] [US3] Write integration tests for complete/incomplete commands in tests/integration/test_cli_status.py

### Implementation for User Story 3 (TDD: GREEN)

- [ ] T037 [US3] Implement TaskService.get() method in src/services/task_service.py
- [ ] T038 [P] [US3] Implement TaskService.complete() method in src/services/task_service.py
- [ ] T039 [P] [US3] Implement TaskService.uncomplete() method in src/services/task_service.py
- [ ] T040 [US3] Implement complete command argparse setup in src/cli/commands.py
- [ ] T041 [US3] Implement incomplete command argparse setup in src/cli/commands.py
- [ ] T042 [US3] Implement complete command handler in src/cli/commands.py
- [ ] T043 [US3] Implement incomplete command handler in src/cli/commands.py
- [ ] T044 [US3] Add TaskNotFoundError handling for complete/incomplete commands

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Users can update task title and/or description by ID

**Independent Test**: Add task, update title/description, view to verify changes saved

### Tests for User Story 4 (TDD: RED)

- [ ] T045 [P] [US4] Write unit tests for TaskService.update() method in tests/unit/test_task_service.py
- [ ] T046 [P] [US4] Write unit tests for update command validation in tests/unit/test_commands.py
- [ ] T047 [P] [US4] Write integration tests for update command in tests/integration/test_cli_update.py

### Implementation for User Story 4 (TDD: GREEN)

- [ ] T048 [US4] Implement TaskService.update() method in src/services/task_service.py
- [ ] T049 [US4] Implement update command argparse setup with --title and --description options in src/cli/commands.py
- [ ] T050 [US4] Implement update command handler in src/cli/commands.py
- [ ] T051 [US4] Add validation for update command (require at least one of title/description)
- [ ] T052 [US4] Add TaskNotFoundError handling for update command

**Checkpoint**: User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can delete tasks by ID, IDs are never reused

**Independent Test**: Add tasks, delete one by ID, verify removed from list, verify ID not reused

### Tests for User Story 5 (TDD: RED)

- [ ] T053 [P] [US5] Write unit tests for TaskService.delete() method in tests/unit/test_task_service.py
- [ ] T054 [P] [US5] Write unit tests for ID non-reuse after deletion in tests/unit/test_task_service.py
- [ ] T055 [P] [US5] Write unit tests for delete command in tests/unit/test_commands.py
- [ ] T056 [P] [US5] Write integration tests for delete command in tests/integration/test_cli_delete.py

### Implementation for User Story 5 (TDD: GREEN)

- [ ] T057 [US5] Implement TaskService.delete() method in src/services/task_service.py
- [ ] T058 [US5] Implement delete command argparse setup in src/cli/commands.py
- [ ] T059 [US5] Implement delete command handler in src/cli/commands.py
- [ ] T060 [US5] Add TaskNotFoundError handling for delete command

**Checkpoint**: All 5 user stories should now be independently functional

---

## Phase 8: CLI Entry Point & Integration

**Purpose**: Complete CLI application with all commands integrated

- [ ] T061 Implement create_parser() function with all subcommands in src/cli/commands.py
- [ ] T062 Implement execute_command() function to route to handlers in src/cli/commands.py
- [ ] T063 Implement main() function with error handling in src/main.py
- [ ] T064 Add startup warning message to main() ("Warning: data stored in memory...")
- [ ] T065 Add --help documentation for all commands
- [ ] T066 Write end-to-end integration test for full workflow in tests/integration/test_full_workflow.py

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T067 [P] Add type hints to all public functions in src/models/task.py
- [ ] T068 [P] Add type hints to all public functions in src/services/task_service.py
- [ ] T069 [P] Add type hints to all public functions in src/cli/commands.py
- [ ] T070 [P] Add type hints to all public functions in src/cli/formatter.py
- [ ] T071 [P] Add docstrings to all modules in src/
- [ ] T072 [P] Add docstrings to all public functions in src/
- [ ] T073 Run ruff check on entire codebase and fix linting issues
- [ ] T074 Run ruff format on entire codebase
- [ ] T075 Run pytest with coverage report, ensure 80%+ coverage
- [ ] T076 Fix any failing tests or coverage gaps
- [ ] T077 Create README.md with setup instructions and usage examples
- [ ] T078 Update CLAUDE.md with project-specific implementation notes
- [ ] T079 Test all 5 commands end-to-end manually
- [ ] T080 Verify Unicode status indicators display correctly (✓ and ○)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2 → P3 → P3)
- **CLI Integration (Phase 8)**: Depends on all 5 user stories being complete
- **Polish (Phase 9)**: Depends on CLI Integration completion

### User Story Dependencies

- **User Story 1 (P1 - Add)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1 - View)**: Can start after Foundational (Phase 2) - No dependencies on other stories (but works best with US1)
- **User Story 3 (P2 - Complete)**: Requires TaskService.get() - minimal dependency
- **User Story 4 (P3 - Update)**: Requires TaskService.get() - minimal dependency
- **User Story 5 (P3 - Delete)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each Phase (TDD Workflow)

1. **Tests FIRST**: All test tasks must be written and FAIL before implementation
2. **Implementation**: Implement to make tests pass (GREEN)
3. **Refactor**: Clean up code while keeping tests passing
4. **Checkpoint**: Verify story works independently before moving to next story

### Parallel Opportunities

**Setup Phase (can run in parallel)**:
- T003 and T004 (create __init__.py files)
- T006 and T007 (.gitignore and dependency installation)

**Foundational Phase (can run in parallel)**:
- T008 (exceptions) can run independently

**Within Each User Story (can run in parallel)**:
- Test files for different modules [P]
- Unit tests vs integration tests [P]

**Between User Stories (can run in parallel after Foundational)**:
- US1 and US2 can be developed simultaneously by different developers
- US3, US4, US5 can start once US1/US2 have TaskService.get() implemented

**Polish Phase (can run in parallel)**:
- T067-T072 (type hints and docstrings for different files)

---

## Parallel Example: Foundational Phase

```bash
# These test tasks can run in parallel (different files):
T014 [P] [US1] Write unit tests for TaskService.add()
T015 [P] [US1] Write unit tests for add command validation
T016 [P] [US1] Write integration test for add command

# After tests fail, implement sequentially:
T017 [US1] Implement TaskService.add()
T018 [US1] Implement add command argparse setup
T019 [US1] Implement add command handler
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (View Tasks)
5. Complete Phase 8: CLI Entry Point (for US1 & US2 only)
6. **STOP and VALIDATE**: Test add + list workflow independently
7. Deploy/demo if ready

**This gives you a working MVP**: users can add tasks and view them!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 + 2 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 → Test independently → Deploy/Demo (Status tracking)
4. Add User Story 4 → Test independently → Deploy/Demo (Task editing)
5. Add User Story 5 → Test independently → Deploy/Demo (Full CRUD)
6. Complete Phase 8 → Full CLI integration
7. Complete Phase 9 → Polish and quality

Each increment adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Add) + User Story 2 (View) → MVP
   - Developer B: User Story 3 (Complete/Incomplete)
   - Developer C: User Story 4 (Update) + User Story 5 (Delete)
3. Integration engineer: Phase 8 (CLI Entry Point)
4. Team: Phase 9 (Polish) together

---

## TDD Workflow Reminder

**For EVERY implementation task:**

1. **RED**: Write test first, run it, watch it FAIL
2. **GREEN**: Write minimal code to make test PASS
3. **REFACTOR**: Clean up code while keeping tests GREEN

**Example for T014-T017 (Add Task)**:

```bash
# RED: Write failing test
- [ ] T014 [P] [US1] Write unit tests for TaskService.add() in tests/unit/test_task_service.py
$ pytest tests/unit/test_task_service.py::test_add_task
# Test fails: ImportError (TaskService doesn't exist yet)

# GREEN: Implement minimal code
- [ ] T017 [US1] Implement TaskService.add() in src/services/task_service.py
$ pytest tests/unit/test_task_service.py::test_add_task
# Test passes!

# REFACTOR: Clean up if needed (while tests stay green)
```

---

## Notes

- All [P] tasks can run in parallel (different files, no dependencies)
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail (RED) before implementing (GREEN)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution requires 80%+ test coverage - validate with: `pytest --cov=src --cov-report=term`

---

## Task Count Summary

**Total Tasks**: 80

**By Phase**:
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 6 tasks
- Phase 3 (US1 - Add): 7 tasks
- Phase 4 (US2 - View): 10 tasks
- Phase 5 (US3 - Complete): 14 tasks
- Phase 6 (US4 - Update): 8 tasks
- Phase 7 (US5 - Delete): 8 tasks
- Phase 8 (CLI Integration): 6 tasks
- Phase 9 (Polish): 14 tasks

**By User Story**:
- User Story 1 (Add): 7 tasks
- User Story 2 (View): 10 tasks
- User Story 3 (Complete/Incomplete): 14 tasks
- User Story 4 (Update): 8 tasks
- User Story 5 (Delete): 8 tasks
- Infrastructure (Setup + Foundational + CLI + Polish): 33 tasks

**Parallel Opportunities**: 32 tasks marked [P] can run in parallel

**Estimated Time**: ~5-8 hours for complete implementation (with TDD)
