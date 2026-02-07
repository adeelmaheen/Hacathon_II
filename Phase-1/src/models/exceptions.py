"""Custom exceptions for todo application."""


class TodoError(Exception):
    """Base exception for todo application."""

    pass


class TaskNotFoundError(TodoError):
    """Raised when a task with given ID doesn't exist."""

    pass


class ValidationError(TodoError):
    """Raised when input validation fails."""

    pass
