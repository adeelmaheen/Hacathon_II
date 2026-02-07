# Todo CLI Application

A simple command-line todo application that stores tasks in memory using Python. Built following Test-Driven Development (TDD) and Spec-Driven Development principles.

## Features

✅ **Add tasks** with title and description
✅ **View all tasks** with status indicators (✓ complete / ○ incomplete)
✅ **Mark tasks** as complete or incomplete
✅ **Update task** title and/or description
✅ **Delete tasks** by ID

## Requirements

- Python 3.13+
- UV package manager (recommended) or pip

## Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd hackhathon_II

# Install dependencies
uv pip install -e ".[dev]"
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd hackhathon_II

# Install dependencies
pip install -e ".[dev]"
```

## Usage

The application runs in interactive mode. Start it with:

```bash
python -m src.main
```

You'll see a menu with options to manage your tasks:

```
==================================================
TODO CLI - Main Menu
==================================================
1. Add a new task
2. View all tasks
3. Mark task as complete
4. Mark task as incomplete
5. Update task
6. Delete task
7. Exit
==================================================
```

### Interactive Operations

#### Add a Task

Select option `1` from the menu, then:
- Enter the task title when prompted
- Optionally enter a description (or press Enter to skip)

Example:
```
Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, bread

Task added successfully!
ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: [ ] Incomplete
```

#### View All Tasks

Select option `2` from the menu to see all tasks:

```
ID  Status  Title                Description
==  ======  ===================  ==============================
1   ○       Buy groceries        Milk, eggs, bread
2   ✓       Call dentist         Schedule 6-month cleaning
3   ○       Review PR #42
```

#### Mark Task as Complete

Select option `3` from the menu, then enter the task ID when prompted.

#### Mark Task as Incomplete

Select option `4` from the menu, then enter the task ID when prompted.

#### Update Task

Select option `5` from the menu, then:
- Enter the task ID
- See the current task details
- Enter new values (or press Enter to keep current value)

#### Delete Task

Select option `6` from the menu, then:
- Enter the task ID
- Confirm deletion when prompted with `yes` or `y`

#### Exit

Select option `7` to exit the application. All tasks will be lost as they are stored in memory only.

## Running Tests

The project uses pytest for testing with TDD (Test-Driven Development) approach.

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=src --cov-report=term-missing
```

### Run Specific Test Files

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Specific test file
pytest tests/unit/test_task.py
```

## Code Quality

### Linting

```bash
ruff check src/ tests/
```

### Formatting

```bash
ruff format src/ tests/
```

## Project Structure

```
hackhathon_II/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task entity with validation
│   │   └── exceptions.py    # Custom exceptions
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic (CRUD operations)
│   └── cli/
│       ├── __init__.py
│       ├── commands.py      # CLI command definitions
│       └── formatter.py     # Output formatting
├── tests/
│   ├── __init__.py
│   ├── unit/                # Unit tests
│   │   ├── test_task.py
│   │   └── test_task_service.py
│   └── integration/         # Integration tests
│       └── (integration test files)
├── specs/                   # Design specifications
│   └── 001-todo-cli/
│       ├── spec.md          # Feature specification
│       ├── plan.md          # Implementation plan
│       ├── tasks.md         # Task breakdown
│       ├── data-model.md    # Data model documentation
│       ├── research.md      # Technical research
│       ├── quickstart.md    # Implementation guide
│       └── contracts/       # API/CLI contracts
├── .specify/                # SpecKit Plus configuration
├── pyproject.toml           # Project configuration
├── README.md                # This file
└── CLAUDE.md                # Claude Code instructions

```

## Important Notes

⚠️ **In-Memory Storage**: All data is stored in memory and will be lost when the application exits. This is by design for Phase 1.

⚠️ **Task IDs**: Once a task is deleted, its ID is never reused. IDs always increment.

⚠️ **No Persistence**: There is no database or file storage. Tasks exist only while the application is running.

## Development Workflow

This project follows Spec-Driven Development (SDD) using SpecKit Plus:

1. ✅ **Specification** (`/sp.specify`) - Define user requirements
2. ✅ **Planning** (`/sp.plan`) - Create technical architecture
3. ✅ **Tasks** (`/sp.tasks`) - Break down implementation
4. ✅ **Implementation** (`/sp.implement`) - Build with TDD

### TDD Workflow

Every feature follows Red-Green-Refactor:

1. **RED**: Write failing tests
2. **GREEN**: Write minimal code to pass tests
3. **REFACTOR**: Improve code while keeping tests green

## Contributing

This is a learning project demonstrating:
- ✅ Test-Driven Development (TDD)
- ✅ Spec-Driven Development (SDD)
- ✅ Clean Code principles
- ✅ Python best practices
- ✅ Type hints and documentation
- ✅ Proper project structure

## License

This project is created for educational purposes.

## Contact

For questions or feedback, please refer to the project documentation in the `specs/` directory.

---

Built with ❤️ using Claude Code and SpecKit Plus
