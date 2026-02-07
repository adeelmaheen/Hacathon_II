# Research: Todo CLI Application

**Feature**: 001-todo-cli
**Date**: 2026-01-01
**Phase**: 0 - Research & Technology Decisions

## Overview

This document consolidates research findings and technology decisions for the Todo CLI application. Since this is a simple console application with minimal external dependencies, most decisions are straightforward and aligned with Python best practices.

## Technology Decisions

### 1. CLI Framework Selection

**Decision**: Use Python's built-in `argparse` module

**Rationale**:
- **Simplicity First Principle**: No external dependencies needed for basic CLI parsing
- **Standard Library**: Part of Python 3.13+, well-documented and stable
- **Sufficient Features**: Supports subcommands, arguments, help text generation
- **Zero Learning Curve**: Widely known, simple API

**Alternatives Considered**:
- **Click**: Popular CLI framework with decorator-based API
  - Rejected: Adds external dependency, more complex than needed for 5 simple commands
- **Typer**: Modern CLI framework with type hints
  - Rejected: External dependency, overkill for simple CRUD operations
- **argparse**: ✅ Selected - Built-in, simple, sufficient

**Implementation Notes**:
- Use subparsers for each of the 5 commands
- Leverage argparse's automatic help generation
- Type conversion and validation handled by argparse + custom validators

---

### 2. In-Memory Data Structure

**Decision**: Use Python dictionary with integer keys for tasks, maintain separate counter for ID generation

**Rationale**:
- **Fast Lookup**: O(1) access by task ID
- **Simple**: Native Python data structure, no serialization needed
- **Flexible**: Easy to add/remove tasks, maintain order by ID
- **ID Management**: Separate counter ensures no ID reuse after deletion

**Alternatives Considered**:
- **List with sequential indexing**:
  - Rejected: Deletions create gaps, requires reindexing or sparse lists
- **Dictionary with UUID keys**:
  - Rejected: User-facing UUIDs are not user-friendly (spec requires integer IDs)
- **Dictionary with int keys + counter**: ✅ Selected - Best trade-off

**Data Structure**:
```python
# In TaskService class
_tasks: dict[int, Task] = {}  # Task storage
_next_id: int = 1              # ID counter (never decrements)
```

---

### 3. Testing Strategy

**Decision**: pytest with standard assertions, pytest-cov for coverage

**Rationale**:
- **pytest**: Industry standard, simple syntax, excellent fixture support
- **pytest-cov**: Built on coverage.py, integrates seamlessly with pytest
- **Fast**: Constitution requires < 1 second test runtime
- **TDD Support**: Excellent support for test-first development workflow

**Alternatives Considered**:
- **unittest**: Standard library option
  - Rejected: More verbose, class-based structure adds boilerplate
- **pytest**: ✅ Selected - Concise, powerful, widely adopted

**Coverage Goals**:
- Minimum 80% coverage (constitution requirement)
- Target 90%+ coverage for core business logic
- 100% coverage for models and services

---

### 4. Input Validation

**Decision**: Validation in Task model using Python dataclasses with `__post_init__`

**Rationale**:
- **Early Validation**: Catch errors at object creation time
- **Type Safety**: Leverage type hints and dataclass validation
- **Single Responsibility**: Model knows its own validation rules
- **Clear Errors**: Raise ValueError with descriptive messages

**Validation Rules** (from spec):
- Title: Required, 1-500 characters, non-empty after strip
- Description: Optional, 0-2000 characters
- ID: Positive integer
- Status: Boolean (True = complete, False = incomplete)

**Implementation Pattern**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self):
        # Validation logic here
```

---

### 5. Output Formatting

**Decision**: Use simple string formatting with Unicode status indicators

**Rationale**:
- **Spec Requirement**: ✓ for complete, ○ for incomplete
- **Cross-Platform**: Unicode symbols supported on modern terminals
- **Simple**: No external libraries needed (rich, tabulate, etc.)
- **Readable**: Clear visual distinction between statuses

**Format Template**:
```
ID  Status  Title                Description
1   ○       Buy groceries        Milk, eggs, bread
2   ✓       Call dentist         Schedule cleaning
```

**Alternatives Considered**:
- **Rich library**: Beautiful terminal formatting
  - Rejected: External dependency, complexity violation
- **Simple string formatting**: ✅ Selected - Sufficient, no dependencies

---

### 6. Error Handling Strategy

**Decision**: Use custom exception hierarchy with user-friendly messages

**Rationale**:
- **Clear Errors**: Spec requires actionable error messages
- **Separation**: Distinguish between validation errors, not found errors, etc.
- **Graceful Degradation**: CLI should never crash, always provide helpful feedback

**Exception Hierarchy**:
```python
class TodoError(Exception):
    """Base exception for todo app"""

class TaskNotFoundError(TodoError):
    """Raised when task ID doesn't exist"""

class ValidationError(TodoError):
    """Raised when input validation fails"""
```

---

### 7. Project Setup & Dependencies

**Decision**: Use UV for package management with minimal dependencies

**Rationale**:
- **Constitution Requirement**: UV mandated for Python 3.13+
- **Fast**: UV is significantly faster than pip
- **Modern**: Better dependency resolution than pip
- **Simple**: pyproject.toml-based configuration

**Dependencies**:
```toml
[project]
name = "todo-cli"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []  # No runtime dependencies!

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",      # Linting + formatting
]
```

---

### 8. Code Quality Tools

**Decision**: Use Ruff for both linting and formatting

**Rationale**:
- **Speed**: 10-100x faster than pylint/black
- **All-in-One**: Replaces pylint, flake8, isort, black
- **PEP 8 Compliance**: Enforces constitution requirement
- **Type Checking**: Use built-in Python type hints, checked by mypy (optional dev dependency)

**Configuration**:
- Max line length: 100 characters
- Target Python version: 3.13
- Enforce type hints on public functions

---

## Best Practices Summary

### CLI Design Patterns
1. **Command Pattern**: Each operation (add, view, update, delete, complete) is a subcommand
2. **Help First**: Comprehensive help text for each command
3. **Confirmation**: No confirmations for destructive operations (CLI should be scriptable)
4. **Exit Codes**: 0 for success, non-zero for errors

### Python Patterns
1. **Dataclasses**: Use for Task model (immutability not required)
2. **Type Hints**: All public functions and methods
3. **Docstrings**: Google style for consistency
4. **Error Messages**: Always actionable (e.g., "Task ID 99 not found. Use 'list' to see all tasks.")

### Testing Patterns
1. **Arrange-Act-Assert**: Clear test structure
2. **Fixtures**: pytest fixtures for common setup (empty task service, pre-populated tasks)
3. **Parametrize**: Use pytest.mark.parametrize for edge cases
4. **Integration Tests**: Test full CLI workflows end-to-end

---

## Implementation Order Recommendations

Based on research, suggested implementation order:

1. **Task Model** (models/task.py) - Foundation
2. **TaskService** (services/task_service.py) - Business logic
3. **Formatter** (cli/formatter.py) - Output utilities
4. **Commands** (cli/commands.py) - CLI interface
5. **Main** (main.py) - Entry point
6. **Integration** (tests/) - Full workflow tests

This order follows dependency chain and enables incremental testing.

---

## Risks & Mitigations

### Risk 1: Unicode Status Indicators Not Displaying
**Mitigation**: Fall back to ASCII ([ ] and [x]) if terminal doesn't support Unicode
**Decision**: Start with Unicode, document fallback in README

### Risk 2: Performance Degradation with Large Task Lists
**Mitigation**: Dictionary lookup is O(1), should handle 1000+ tasks easily
**Decision**: Implement as planned, benchmark if issues arise

### Risk 3: ID Counter Overflow
**Mitigation**: Python integers have arbitrary precision, practically impossible
**Decision**: No mitigation needed

---

## Open Questions

**None** - All technical decisions are clear and documented above.

---

## References

- [Python argparse documentation](https://docs.python.org/3/library/argparse.html)
- [Python dataclasses guide](https://docs.python.org/3/library/dataclasses.html)
- [pytest documentation](https://docs.pytest.org/)
- [Ruff linter documentation](https://docs.astral.sh/ruff/)
- [UV package manager](https://github.com/astral-sh/uv)
