"""Task service for managing in-memory task storage."""

from src.models.task import Task
from src.models.exceptions import TaskNotFoundError


class TaskService:
    """Manages in-memory task storage and operations.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Counter for generating unique task IDs
    """

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

    def update(self, task_id: int, title: str | None = None,
               description: str | None = None) -> Task:
        """Update task title and/or description.

        Args:
            task_id: ID of task to update
            title: New title (if provided)
            description: New description (if provided)

        Returns:
            The updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
            ValueError: If title or description validation fails
        """
        task = self.get(task_id)

        # Update title if provided
        if title is not None:
            # Create new task to validate, then update
            updated_task = Task(
                id=task.id,
                title=title,
                description=task.description if description is None else description,
                completed=task.completed
            )
            self._tasks[task_id] = updated_task
            return updated_task

        # Update description only
        if description is not None:
            updated_task = Task(
                id=task.id,
                title=task.title,
                description=description,
                completed=task.completed
            )
            self._tasks[task_id] = updated_task
            return updated_task

        return task

    def delete(self, task_id: int) -> None:
        """Delete task by ID.

        Args:
            task_id: ID of task to delete

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError("Task not found")
        del self._tasks[task_id]

    def complete(self, task_id: int) -> Task:
        """Mark task as complete.

        Args:
            task_id: ID of task to complete

        Returns:
            The updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        task = self.get(task_id)
        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=True
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def uncomplete(self, task_id: int) -> Task:
        """Mark task as incomplete.

        Args:
            task_id: ID of task to uncomplete

        Returns:
            The updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        task = self.get(task_id)
        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=False
        )
        self._tasks[task_id] = updated_task
        return updated_task
