# CLI Interface Contract: Todo CLI Application

**Feature**: 001-todo-cli
**Date**: 2026-01-01
**Version**: 1.0.0

## Overview

This document defines the command-line interface contract for the Todo CLI application. All commands, arguments, options, and output formats are specified here.

## Application Entry Point

**Command**: `python -m src.main` or `python src/main.py`

**Global Options**: None (keep it simple)

**Exit Codes**:
- `0`: Success
- `1`: General error (validation, task not found, etc.)
- `2`: Invalid command or arguments

---

## Commands

### 1. Add Task

**Command**: `add`

**Purpose**: Create a new task with title and optional description

**Syntax**:
```bash
python -m src.main add <title> [description]
```

**Arguments**:
- `title` (required, positional): Task title (1-500 characters)
- `description` (optional, positional): Task description (0-2000 characters)

**Examples**:
```bash
# Add task with title only
python -m src.main add "Buy groceries"

# Add task with title and description
python -m src.main add "Buy groceries" "Milk, eggs, bread"

# Title with spaces (requires quotes)
python -m src.main add "Call dentist for appointment"
```

**Success Output**:
```
Task added successfully!
ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: ○ Incomplete
```

**Error Cases**:
| Condition | Error Message | Exit Code |
|-----------|---------------|-----------|
| Empty title | "Error: Title cannot be empty" | 1 |
| Title > 500 chars | "Error: Title must be 500 characters or less" | 1 |
| Description > 2000 chars | "Error: Description must be 2000 characters or less" | 1 |

---

### 2. List Tasks

**Command**: `list`

**Purpose**: Display all tasks with status indicators

**Syntax**:
```bash
python -m src.main list
```

**Arguments**: None

**Examples**:
```bash
python -m src.main list
```

**Success Output** (tasks exist):
```
ID  Status  Title                Description
==  ======  ===================  ==============================
1   ○       Buy groceries        Milk, eggs, bread
2   ✓       Call dentist         Schedule 6-month cleaning
3   ○       Review PR #42
```

**Success Output** (no tasks):
```
No tasks found.
```

**Notes**:
- Tasks sorted by ID (ascending)
- Status indicators: ✓ = complete, ○ = incomplete
- Description column truncated to fit terminal width if needed
- Empty description shows as blank

---

### 3. Update Task

**Command**: `update`

**Purpose**: Modify task title and/or description by ID

**Syntax**:
```bash
python -m src.main update <id> [--title <new_title>] [--description <new_description>]
```

**Arguments**:
- `id` (required, positional): Task ID to update
- `--title` (optional): New title (1-500 characters)
- `--description` (optional): New description (0-2000 characters)

**Examples**:
```bash
# Update title only
python -m src.main update 1 --title "Buy groceries and snacks"

# Update description only
python -m src.main update 1 --description "Milk, eggs, bread, cookies"

# Update both title and description
python -m src.main update 1 --title "Weekly shopping" --description "Everything for the week"
```

**Success Output**:
```
Task updated successfully!
ID: 1
Title: Weekly shopping
Description: Everything for the week
Status: ○ Incomplete
```

**Error Cases**:
| Condition | Error Message | Exit Code |
|-----------|---------------|-----------|
| Task not found | "Error: Task not found" | 1 |
| Invalid ID | "Error: Invalid task ID" | 1 |
| No updates provided | "Error: Provide --title and/or --description" | 2 |
| Empty title | "Error: Title cannot be empty" | 1 |
| Title > 500 chars | "Error: Title must be 500 characters or less" | 1 |
| Description > 2000 chars | "Error: Description must be 2000 characters or less" | 1 |

---

### 4. Delete Task

**Command**: `delete`

**Purpose**: Remove task by ID

**Syntax**:
```bash
python -m src.main delete <id>
```

**Arguments**:
- `id` (required, positional): Task ID to delete

**Examples**:
```bash
python -m src.main delete 1
```

**Success Output**:
```
Task deleted successfully!
ID: 1
```

**Error Cases**:
| Condition | Error Message | Exit Code |
|-----------|---------------|-----------|
| Task not found | "Error: Task not found" | 1 |
| Invalid ID | "Error: Invalid task ID" | 1 |

**Notes**:
- No confirmation prompt (destructive but scriptable)
- Deleted task IDs are never reused

---

### 5. Mark Complete

**Command**: `complete`

**Purpose**: Mark task as complete (toggle status to done)

**Syntax**:
```bash
python -m src.main complete <id>
```

**Arguments**:
- `id` (required, positional): Task ID to mark complete

**Examples**:
```bash
python -m src.main complete 1
```

**Success Output**:
```
Task marked as complete!
ID: 1
Title: Buy groceries
Status: ✓ Complete
```

**Error Cases**:
| Condition | Error Message | Exit Code |
|-----------|---------------|-----------|
| Task not found | "Error: Task not found" | 1 |
| Invalid ID | "Error: Invalid task ID" | 1 |

**Notes**:
- Idempotent: completing an already-complete task succeeds (no error)

---

### 6. Mark Incomplete

**Command**: `incomplete`

**Purpose**: Mark task as incomplete (toggle status to todo)

**Syntax**:
```bash
python -m src.main incomplete <id>
```

**Arguments**:
- `id` (required, positional): Task ID to mark incomplete

**Examples**:
```bash
python -m src.main incomplete 2
```

**Success Output**:
```
Task marked as incomplete!
ID: 2
Title: Call dentist
Status: ○ Incomplete
```

**Error Cases**:
| Condition | Error Message | Exit Code |
|-----------|---------------|-----------|
| Task not found | "Error: Task not found" | 1 |
| Invalid ID | "Error: Invalid task ID" | 1 |

**Notes**:
- Idempotent: un-completing an already-incomplete task succeeds (no error)

---

## Help Command

**Command**: `--help` or `-h`

**Purpose**: Display usage information

**Syntax**:
```bash
python -m src.main --help
python -m src.main <command> --help
```

**Examples**:
```bash
# Global help
python -m src.main --help

# Command-specific help
python -m src.main add --help
```

**Help Output** (global):
```
usage: todo [-h] {add,list,update,delete,complete,incomplete} ...

Todo CLI - In-memory task management

positional arguments:
  {add,list,update,delete,complete,incomplete}
    add                 Add a new task
    list                List all tasks
    update              Update task details
    delete              Delete a task
    complete            Mark task as complete
    incomplete          Mark task as incomplete

options:
  -h, --help            show this help message and exit

Warning: This application stores data in memory. All tasks will be lost when you exit.
```

---

## Output Format Standards

### Success Messages
- Start with action confirmation: "Task [action] successfully!"
- Include relevant task details (ID at minimum)
- Use consistent formatting

### Error Messages
- Start with "Error: "
- Provide actionable information
- No stack traces in production (log to stderr if needed)

### Status Indicators
- Complete: ✓ (Unicode U+2713)
- Incomplete: ○ (Unicode U+25CB)
- Fallback (if Unicode fails): [x] and [ ]

### Table Formatting
```
Column Header    Alignment    Width
ID               Right        4 chars
Status           Center       6 chars
Title            Left         30 chars (truncate with ...)
Description      Left         40 chars (truncate with ...)
```

---

## Startup Behavior

**On Launch**:
1. Display warning message (stderr):
   ```
   Warning: This application stores data in memory. All tasks will be lost when you exit.
   ```
2. Process command
3. Exit with appropriate code

**Notes**:
- No interactive mode (commands are one-shot)
- No configuration files
- No persistent state

---

## Input Parsing Rules

### Quotes
- Titles/descriptions with spaces MUST be quoted
- Single quotes or double quotes accepted
- Nested quotes must be escaped

### Special Characters
- Unicode characters allowed in title/description
- Newlines in arguments replaced with spaces
- Tab characters replaced with spaces

### ID Format
- Must be positive integer
- No leading zeros
- No decimal points
- Error on invalid format

---

## Error Handling Contract

**All errors must**:
1. Print to stderr (not stdout)
2. Use consistent "Error: <message>" format
3. Exit with non-zero code
4. Never crash with unhandled exception

**Error Precedence**:
1. Invalid command → Exit 2
2. Invalid arguments → Exit 2
3. Validation error → Exit 1
4. Task not found → Exit 1

---

## Performance Contract

**Response Time**:
- Add: < 10ms
- List: < 100ms (for 1000 tasks)
- Update/Delete/Complete: < 10ms
- Help: < 50ms

**Memory Usage**:
- < 10MB for 1000 tasks
- No memory leaks (tasks released on delete)

---

## Backward Compatibility

**Version**: 1.0.0 (initial version)

**Future Changes**:
- Commands never removed (deprecation only)
- Arguments may be added (with defaults)
- Output format may be enhanced (but not broken)
- Error messages may be improved (but codes stay same)

---

## Testing Contract

**All commands MUST**:
1. Have unit tests for business logic
2. Have integration tests for CLI parsing
3. Have error case tests
4. Have edge case tests (empty input, max length, etc.)

**Example Integration Test**:
```python
def test_add_task_integration():
    """Test adding a task via CLI."""
    result = subprocess.run(
        ["python", "-m", "src.main", "add", "Test task", "Test description"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Task added successfully!" in result.stdout
    assert "ID: 1" in result.stdout
```

---

## Summary

**Total Commands**: 6 (add, list, update, delete, complete, incomplete)
**Total Arguments**: Varies by command (0-3 per command)
**Exit Codes**: 3 (0=success, 1=error, 2=invalid usage)
**Output Formats**: 2 (success messages, error messages)

This contract ensures consistent, predictable CLI behavior across all operations.
