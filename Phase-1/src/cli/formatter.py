"""Output formatting utilities for CLI."""

from src.models.task import Task


def status_indicator(completed: bool) -> str:
    """Get status indicator for a task.

    Args:
        completed: Whether the task is completed

    Returns:
        Unicode status indicator (✓ for complete, ○ for incomplete)
    """
    return "✓" if completed else "○"


def format_task_list(tasks: list[Task]) -> str:
    """Format a list of tasks for display.

    Args:
        tasks: List of tasks to format

    Returns:
        Formatted string ready for console output
    """
    if not tasks:
        return "No tasks found."

    # Header
    output = []
    output.append("ID  Status  Title                Description")
    output.append("==  ======  ===================  ==============================")

    # Task rows
    for task in tasks:
        status = status_indicator(task.completed)
        title = task.title[:30] if len(task.title) > 30 else task.title
        desc = task.description[:40] if len(task.description) > 40 else task.description

        # Format row with proper spacing
        row = f"{task.id:<4}{status:<8}{title:<21}{desc}"
        output.append(row)

    return "\n".join(output)


def format_task_detail(task: Task) -> str:
    """Format a single task with full details.

    Args:
        task: Task to format

    Returns:
        Formatted string with task details
    """
    status_text = "Complete" if task.completed else "Incomplete"
    status_icon = status_indicator(task.completed)

    lines = [
        f"ID: {task.id}",
        f"Title: {task.title}",
        f"Description: {task.description}",
        f"Status: {status_icon} {status_text}"
    ]

    return "\n".join(lines)
