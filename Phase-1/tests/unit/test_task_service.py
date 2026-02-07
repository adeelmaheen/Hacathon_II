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


class TestTaskServiceInitialization:
    """Test TaskService initialization."""

    def test_init_creates_empty_storage(self, service):
        """Test that TaskService initializes with empty storage."""
        assert len(service.list_all()) == 0

    def test_init_sets_next_id_to_one(self, service):
        """Test that TaskService starts with ID counter at 1."""
        task = service.add("First task")
        assert task.id == 1


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

    def test_add_task_with_empty_title_raises_error(self, service):
        """Test that adding task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.add("")

    def test_add_task_with_long_title_raises_error(self, service):
        """Test that adding task with title > 500 chars raises ValueError."""
        long_title = "x" * 501
        with pytest.raises(ValueError, match="Title must be 500 characters or less"):
            service.add(long_title)


class TestListAllTasks:
    """Test listing all tasks."""

    def test_list_all_empty(self, service):
        """Test listing tasks when none exist."""
        tasks = service.list_all()
        assert tasks == []
        assert len(tasks) == 0

    def test_list_all_returns_all_tasks(self, populated_service):
        """Test that list_all returns all tasks."""
        tasks = populated_service.list_all()
        assert len(tasks) == 3

    def test_list_all_returns_sorted_by_id(self, service):
        """Test that tasks are returned sorted by ID."""
        service.add("Task 3")
        service.add("Task 1")
        service.add("Task 2")
        tasks = service.list_all()
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3


class TestGetTask:
    """Test getting a single task by ID."""

    def test_get_existing_task(self, populated_service):
        """Test getting a task that exists."""
        task = populated_service.get(2)
        assert task.id == 2
        assert task.title == "Task 2"

    def test_get_nonexistent_task_raises_error(self, service):
        """Test that getting non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError, match="Task not found"):
            service.get(999)


class TestCompleteTask:
    """Test marking tasks as complete."""

    def test_complete_task(self, populated_service):
        """Test marking a task as complete."""
        task = populated_service.complete(1)
        assert task.completed is True

    def test_complete_already_complete_task(self, populated_service):
        """Test completing an already complete task (idempotent)."""
        populated_service.complete(1)
        task = populated_service.complete(1)
        assert task.completed is True

    def test_complete_nonexistent_task_raises_error(self, service):
        """Test that completing non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError, match="Task not found"):
            service.complete(999)


class TestUncompleteTask:
    """Test marking tasks as incomplete."""

    def test_uncomplete_task(self, populated_service):
        """Test marking a complete task as incomplete."""
        populated_service.complete(1)
        task = populated_service.uncomplete(1)
        assert task.completed is False

    def test_uncomplete_already_incomplete_task(self, populated_service):
        """Test uncompleting an already incomplete task (idempotent)."""
        task = populated_service.uncomplete(1)
        assert task.completed is False

    def test_uncomplete_nonexistent_task_raises_error(self, service):
        """Test that uncompleting non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError, match="Task not found"):
            service.uncomplete(999)


class TestUpdateTask:
    """Test updating task details."""

    def test_update_title_only(self, populated_service):
        """Test updating only the title."""
        task = populated_service.update(1, title="Updated title")
        assert task.title == "Updated title"
        assert task.description == "Description 1"

    def test_update_description_only(self, populated_service):
        """Test updating only the description."""
        task = populated_service.update(1, description="Updated description")
        assert task.title == "Task 1"
        assert task.description == "Updated description"

    def test_update_both_title_and_description(self, populated_service):
        """Test updating both title and description."""
        task = populated_service.update(1, title="New title", description="New description")
        assert task.title == "New title"
        assert task.description == "New description"

    def test_update_nonexistent_task_raises_error(self, service):
        """Test that updating non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError, match="Task not found"):
            service.update(999, title="New title")

    def test_update_with_invalid_title_raises_error(self, populated_service):
        """Test that updating with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            populated_service.update(1, title="")


class TestDeleteTask:
    """Test deleting tasks."""

    def test_delete_task(self, populated_service):
        """Test deleting a task."""
        populated_service.delete(2)
        tasks = populated_service.list_all()
        assert len(tasks) == 2
        assert all(task.id != 2 for task in tasks)

    def test_delete_nonexistent_task_raises_error(self, service):
        """Test that deleting non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError, match="Task not found"):
            service.delete(999)

    def test_id_not_reused_after_deletion(self, service):
        """Test that deleted task IDs are not reused."""
        service.add("Task 1")
        service.add("Task 2")
        service.delete(1)
        task3 = service.add("Task 3")
        assert task3.id == 3  # Not 1!
