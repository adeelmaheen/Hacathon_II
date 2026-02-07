# Quickstart Guide: Todo CLI Application

**Feature**: 001-todo-cli
**Date**: 2026-01-01
**Audience**: Developers implementing this feature

## Overview

This quickstart guide provides a step-by-step walkthrough for implementing and testing the Todo CLI application. Follow these steps to build the application from scratch using Test-Driven Development (TDD).

---

## Prerequisites

Before starting implementation, ensure you have:

- [x] Python 3.13+ installed
- [x] UV package manager installed (`pip install uv` or system package manager)
- [x] Git repository initialized
- [x] Constitution reviewed (`.specify/memory/constitution.md`)
- [x] Specification reviewed (`specs/001-todo-cli/spec.md`)
- [x] Implementation plan reviewed (`specs/001-todo-cli/plan.md`)
- [x] Data model reviewed (`specs/001-todo-cli/data-model.md`)

---

## Step 1: Project Initialization

### 1.1 Create Project Structure

```bash
# Create source directories
mkdir -p src/models
mkdir -p src/services
mkdir -p src/cli

# Create test directories
mkdir -p tests/unit
mkdir -p tests/integration

# Create __init__.py files
touch src/__init__.py
touch src/models/__init__.py
touch src/services/__init__.py
touch src/cli/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

### 1.2 Initialize UV Project

```bash
# Initialize pyproject.toml
uv init

# Or create manually with this content:
cat > pyproject.toml << 'EOF'
[project]
name = "todo-cli"
version = "0.1.0"
description = "In-memory CLI todo application"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "--cov=src --cov-report=term-missing --cov-report=html"

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
EOF
```

### 1.3 Install Dependencies

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Or with regular pip
pip install -e ".[dev]"
```

### 1.4 Create .gitignore

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
EOF
```

---

## Step 2: Implement Task Model (TDD)

### 2.1 Write Tests First (RED)

Create `tests/unit/test_task.py`:

```python
"""Unit tests for Task model."""

import pytest
from src.models.task import Task


class TestTaskCreation:
    """Test task creation and validation."""

    def test_create_task_with_all_fields(self):
        """Test creating a task with all fields."""
        task = Task(id=1, title="Buy groceries", description="Milk, eggs, bread")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.completed is False

    def test_create_task_with_minimal_fields(self):
        """Test creating a task with only required fields."""
        task = Task(id=1, title="Call dentist")
        assert task.id == 1
        assert task.title == "Call dentist"
        assert task.description == ""
        assert task.completed is False

    def test_create_completed_task(self):
        """Test creating a task that's already completed."""
        task = Task(id=1, title="Old task", completed=True)
        assert task.completed is True


class TestTaskValidation:
    """Test task validation rules."""

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(id=1, title="")

    def test_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(id=1, title="   ")

    def test_title_too_long_raises_error(self):
        """Test that title > 500 chars raises ValueError."""
        long_title = "x" * 501
        with pytest.raises(ValueError, match="Title must be 500 characters or less"):
            Task(id=1, title=long_title)

    def test_description_too_long_raises_error(self):
        """Test that description > 2000 chars raises ValueError."""
        long_desc = "x" * 2001
        with pytest.raises(ValueError, match="Description must be 2000 characters or less"):
            Task(id=1, title="Valid title", description=long_desc)

    def test_invalid_id_raises_error(self):
        """Test that ID <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            Task(id=0, title="Valid title")

        with pytest.raises(ValueError, match="Invalid task ID"):
            Task(id=-1, title="Valid title")

    def test_max_valid_title_length(self):
        """Test that title with exactly 500 chars is valid."""
        title = "x" * 500
        task = Task(id=1, title=title)
        assert len(task.title) == 500

    def test_max_valid_description_length(self):
        """Test that description with exactly 2000 chars is valid."""
        desc = "x" * 2000
        task = Task(id=1, title="Valid", description=desc)
        assert len(task.description) == 2000
```

### 2.2 Run Tests (RED - they should fail)

```bash
pytest tests/unit/test_task.py -v
```

Expected: All tests fail with ImportError or AttributeError.

### 2.3 Implement Task Model (GREEN)

Create `src/models/task.py`:

```python
"""Task model for todo application."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique positive integer identifier
        title: Task title (1-500 characters, required)
        description: Optional task description (0-2000 characters)
        completed: Completion status (default: False)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate task fields after initialization.

        Raises:
            ValueError: If any field fails validation
        """
        # Validate ID
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Invalid task ID")

        # Validate title
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")

        if len(self.title) > 500:
            raise ValueError("Title must be 500 characters or less")

        # Validate description
        if len(self.description) > 2000:
            raise ValueError("Description must be 2000 characters or less")
```

### 2.4 Run Tests Again (GREEN - they should pass)

```bash
pytest tests/unit/test_task.py -v --cov=src/models
```

Expected: All tests pass with 100% coverage for `task.py`.

### 2.5 Refactor (if needed)

Review code for improvements. For this simple model, likely no refactoring needed.

---

## Step 3: Implement TaskService (TDD)

### 3.1 Write Tests First (RED)

Create `tests/unit/test_task_service.py`:

```python
"""Unit tests for TaskService."""

import pytest
from src.services.task_service import TaskService, TaskNotFoundError
from src.models.task import Task


@pytest.fixture
def service():
    """Provide a fresh TaskService instance for each test."""
    return TaskService()


@pytest.fixture
def populated_service():
    """Provide a TaskService with some tasks."""
    svc = TaskService()
    svc.add("Task 1", "Description 1")
    svc.add("Task 2", "Description 2")
    svc.add("Task 3")
    return svc


class TestAddTask:
    """Test adding tasks."""

    def test_add_task_with_description(self, service):
        """Test adding a task with description."""
        task = service.add("Buy groceries", "Milk, eggs, bread")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.completed is False

    def test_add_task_without_description(self, service):
        """Test adding a task without description."""
        task = service.add("Call dentist")
        assert task.id == 1
        assert task.title == "Call dentist"
        assert task.description == ""

    def test_add_multiple_tasks_increments_id(self, service):
        """Test that adding multiple tasks increments IDs."""
        task1 = service.add("Task 1")
        task2 = service.add("Task 2")
        task3 = service.add("Task 3")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3


# ... (Add more test classes for list, get, update, delete, complete, uncomplete)
# See full test file in implementation
```

### 3.2 Implement TaskService (GREEN)

Create `src/services/task_service.py`:

```python
"""Task service for managing in-memory task storage."""

from src.models.task import Task


class TaskNotFoundError(Exception):
    """Raised when a task with given ID doesn't exist."""


class TaskService:
    """Manages in-memory task storage and operations."""

    def __init__(self) -> None:
        """Initialize empty task storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, title: str, description: str = "") -> Task:
        """Add a new task.

        Args:
            title: Task title (1-500 characters)
            description: Optional task description (0-2000 characters)

        Returns:
            The created Task object

        Raises:
            ValueError: If title or description validation fails
        """
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        """Get task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            The Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError("Task not found")
        return self._tasks[task_id]

    def list_all(self) -> list[Task]:
        """Get all tasks sorted by ID.

        Returns:
            List of all tasks (empty list if no tasks)
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    # ... (Implement update, delete, complete, uncomplete methods)
```

### 3.3 Run Tests (GREEN)

```bash
pytest tests/unit/test_task_service.py -v --cov=src/services
```

---

## Step 4: Implement CLI Commands (TDD)

### 4.1 Implement Formatter First

Create tests and implementation for `src/cli/formatter.py` (handles output formatting).

### 4.2 Implement Commands

Create tests and implementation for `src/cli/commands.py` (argparse setup and command handlers).

### 4.3 Implement Main Entry Point

Create `src/main.py`:

```python
"""Main entry point for Todo CLI application."""

import sys
from src.cli.commands import create_parser, execute_command


def main() -> int:
    """Run the todo CLI application.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Display warning message
    print(
        "Warning: This application stores data in memory. "
        "All tasks will be lost when you exit.",
        file=sys.stderr
    )

    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # Execute command
    try:
        execute_command(args)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## Step 5: Integration Testing

Create `tests/integration/test_cli_integration.py` with end-to-end workflow tests.

---

## Step 6: Verification Checklist

Before marking implementation complete, verify:

- [ ] All unit tests pass (`pytest tests/unit -v`)
- [ ] All integration tests pass (`pytest tests/integration -v`)
- [ ] Code coverage ≥ 80% (`pytest --cov=src --cov-report=term`)
- [ ] All files have type hints (`ruff check src/`)
- [ ] Code is formatted (`ruff format src/ tests/`)
- [ ] All 5 commands work end-to-end
- [ ] Error messages are user-friendly
- [ ] Status indicators display correctly (✓ and ○)
- [ ] README.md created with usage instructions
- [ ] CLAUDE.md updated with project-specific guidance

---

## Common Issues & Solutions

### Issue 1: Unicode Characters Not Displaying

**Solution**: Check terminal encoding. Add ASCII fallback in formatter:

```python
try:
    return "✓" if completed else "○"
except UnicodeEncodeError:
    return "[x]" if completed else "[ ]"
```

### Issue 2: Tests Fail on Windows

**Solution**: Use `sys.executable` in integration tests instead of hardcoded `python`:

```python
subprocess.run([sys.executable, "-m", "src.main", "add", "Test"])
```

### Issue 3: Import Errors

**Solution**: Ensure all `__init__.py` files exist and package is installed in editable mode (`pip install -e .`).

---

## Next Steps

After completing implementation:

1. Run `/sp.tasks` to generate task breakdown (if not done yet)
2. Mark all tasks complete in tasks.md
3. Create pull request with constitution compliance verification
4. Record implementation in PHR (Prompt History Record)

---

## Time Estimates

| Phase | Estimated Time |
|-------|---------------|
| Project setup | 15 minutes |
| Task model (TDD) | 30 minutes |
| TaskService (TDD) | 1 hour |
| Formatter (TDD) | 30 minutes |
| CLI commands (TDD) | 1.5 hours |
| Integration tests | 45 minutes |
| Documentation | 30 minutes |
| **Total** | **~5 hours** |

---

## Success Criteria

Implementation is complete when:

1. All 5 operations work correctly
2. All tests pass (unit + integration)
3. Code coverage ≥ 80%
4. Constitution compliance verified
5. Documentation complete (README, CLAUDE.md)
6. Code quality standards met (type hints, linting, formatting)

---

## Reference Files

- Constitution: `.specify/memory/constitution.md`
- Specification: `specs/001-todo-cli/spec.md`
- Implementation Plan: `specs/001-todo-cli/plan.md`
- Data Model: `specs/001-todo-cli/data-model.md`
- CLI Contract: `specs/001-todo-cli/contracts/cli-interface.md`

Happy coding! 🚀
