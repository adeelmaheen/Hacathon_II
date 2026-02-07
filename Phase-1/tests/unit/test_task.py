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
