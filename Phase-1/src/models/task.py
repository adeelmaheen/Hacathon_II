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
