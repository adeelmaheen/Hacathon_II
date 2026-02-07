<!--
Sync Impact Report:
- Version change: None → 1.0.0 (Initial constitution)
- Modified principles: N/A (new document)
- Added sections: All sections (initial creation)
- Removed sections: None
- Templates requiring updates:
  ✅ plan-template.md (reviewed - compatible)
  ✅ spec-template.md (reviewed - compatible)
  ✅ tasks-template.md (reviewed - compatible)
- Follow-up TODOs: None
-->

# Phase 1 Todo App Constitution

## Core Principles

### I. Simplicity First

Every component MUST be as simple as possible while meeting requirements. This is a basic-level CLI todo app—no over-engineering allowed.

- Start with the simplest solution that works
- No premature abstractions or frameworks
- No features beyond the 5 core operations (add, delete, update, view, mark completed)
- YAGNI (You Aren't Gonna Need It) strictly enforced

**Rationale**: Phase 1 is about demonstrating clean fundamentals, not complex architecture. Keep it learnable and maintainable.

### II. In-Memory Storage (Non-Negotiable)

All task data MUST be stored in memory using Python data structures. NO databases, NO file persistence.

- Use Python lists/dictionaries for task storage
- Data resets on application restart
- No SQLite, JSON files, pickle, or any persistence layer
- Simple, direct data access

**Rationale**: Phase 1 requirement explicitly states in-memory storage. This constraint keeps the focus on core operations and clean code structure.

### III. Test-First Development (TDD)

Tests MUST be written before implementation. Red-Green-Refactor cycle is mandatory.

- Write test → Test fails (Red) → Implement → Test passes (Green) → Refactor
- Every feature MUST have corresponding tests
- Tests verify expected behavior before code exists
- Use pytest as the testing framework

**Rationale**: TDD ensures code quality, prevents bugs, and serves as living documentation. Required by project guidelines.

### IV. Clean Python Project Structure

Project MUST follow Python best practices and proper organization.

- Use UV for dependency management (Python 3.13+)
- Source code in `/src` directory
- Tests in `/tests` directory
- Clear separation of concerns: models, services, CLI interface
- Follow PEP 8 style guidelines
- Type hints required for all functions

**Rationale**: Professional project structure demonstrates software engineering competency and makes code maintainable.

### V. Spec-Driven Development with SpecKit Plus

All development MUST follow Spec-Driven Development workflow using SpecKit Plus tools.

- Feature specification created first (`/sp.specify`)
- Implementation plan follows spec (`/sp.plan`)
- Tasks derived from plan (`/sp.tasks`)
- Implementation executes tasks (`/sp.implement`)
- All artifacts stored in proper directories

**Rationale**: Ensures systematic development, clear documentation, and traceability from requirements to implementation.

### VI. Five Core Operations Only

The application MUST implement exactly these operations, no more, no less:

1. **Add Task**: Create new task with title and description
2. **View Tasks**: List all tasks with status indicators (✓ complete / ○ incomplete)
3. **Update Task**: Modify task title or description by ID
4. **Delete Task**: Remove task by ID
5. **Mark Complete/Incomplete**: Toggle task completion status by ID

**Rationale**: Phase 1 scope is clearly defined. Additional features dilute focus and increase complexity unnecessarily.

## Technology Stack Requirements

### Mandatory Technologies

- **Python**: 3.13+ (latest stable)
- **UV**: Package and project management
- **pytest**: Testing framework
- **Claude Code**: AI pair programming tool
- **SpecKit Plus**: Spec-driven development framework

### Prohibited Technologies

- No web frameworks (Flask, FastAPI, Django)
- No databases (SQLite, PostgreSQL, MongoDB)
- No file persistence (JSON, pickle, CSV)
- No GUI frameworks
- No external task management libraries

**Rationale**: Keep dependencies minimal. This is a console application demonstrating fundamentals.

## Development Workflow

### 1. Specification Phase

- Use `/sp.specify` to create feature specification
- Define user scenarios with acceptance criteria
- Identify all functional requirements
- Store in `/specs/<feature>/spec.md`

### 2. Planning Phase

- Use `/sp.plan` to create implementation plan
- Define technical architecture
- Document data models
- Identify file structure
- Store in `/specs/<feature>/plan.md`

### 3. Task Generation

- Use `/sp.tasks` to generate task breakdown
- Tasks MUST be specific and testable
- Include clear file paths
- Mark parallel opportunities
- Store in `/specs/<feature>/tasks.md`

### 4. Implementation Phase

- Use `/sp.implement` to execute tasks
- Write tests first (TDD)
- Implement minimum code to pass tests
- Refactor for clarity
- Commit frequently with clear messages

### 5. Documentation

- Record all interactions in Prompt History Records (PHRs)
- Create ADRs for architectural decisions
- Maintain README.md with setup instructions
- Update CLAUDE.md with project-specific guidance

## Quality Standards

### Code Quality

- All code MUST pass linting (ruff or pylint)
- All code MUST be formatted (black or ruff format)
- Type hints MUST be present for all public functions
- Maximum function complexity: 10 (cyclomatic complexity)
- No duplicate code (DRY principle)

### Testing Standards

- Minimum 80% code coverage
- All happy paths MUST be tested
- All error conditions MUST be tested
- Edge cases MUST be identified and tested
- Tests MUST be fast (< 1 second total runtime for Phase 1)

### Documentation Standards

- All modules MUST have docstrings
- All public functions MUST have docstrings
- README.md MUST include:
  - Project description
  - Setup instructions
  - Usage examples
  - Running tests
  - Project structure
- CLAUDE.md MUST include Claude Code specific instructions

## Deliverables Checklist

Phase 1 is complete when ALL of the following exist:

- [ ] GitHub repository initialized
- [ ] `.specify/memory/constitution.md` (this file)
- [ ] `specs/<feature>/` folder with spec.md, plan.md, tasks.md
- [ ] `history/prompts/` folder with all PHRs
- [ ] `src/` folder with Python source code
- [ ] `tests/` folder with pytest tests
- [ ] `README.md` with setup instructions
- [ ] `CLAUDE.md` with Claude Code instructions
- [ ] Working console app demonstrating all 5 operations
- [ ] All tests passing
- [ ] Code meets quality standards

## Governance

### Amendment Process

1. Identify need for constitutional change
2. Document proposed change with rationale
3. Verify impact on existing templates and artifacts
4. Update constitution with version bump:
   - MAJOR: Breaking changes to principles or workflow
   - MINOR: New principles or significant additions
   - PATCH: Clarifications, corrections, minor refinements
5. Update dependent templates (plan, spec, tasks)
6. Create ADR if architecturally significant
7. Update LAST_AMENDED_DATE

### Compliance Review

- All PRs MUST verify compliance with this constitution
- Any deviation MUST be justified in writing
- Constitution supersedes all other practices
- Complexity MUST be justified or eliminated
- Use CLAUDE.md for runtime development guidance that doesn't require constitutional amendments

### Version History

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01

#### Changelog

- **1.0.0** (2026-01-01): Initial constitution for Phase 1 Todo App
  - Established 6 core principles
  - Defined technology stack constraints
  - Documented spec-driven workflow
  - Set quality standards and deliverables
