"""CLI command definitions and handlers."""

import argparse
import sys
from typing import Any

from src.services.task_service import TaskService
from src.models.exceptions import TaskNotFoundError
from src.cli.formatter import format_task_list, format_task_detail


# Global service instance (in-memory storage)
_service = TaskService()


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser with all subcommands
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Todo CLI - In-memory task management"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("description", nargs="?", default="", help="Task description (optional)")

    # List command
    subparsers.add_parser("list", help="List all tasks")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update task details")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--description", help="New description")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # Incomplete command
    incomplete_parser = subparsers.add_parser("incomplete", help="Mark task as incomplete")
    incomplete_parser.add_argument("id", type=int, help="Task ID")

    return parser


def handle_add(args: Any) -> None:
    """Handle add command.

    Args:
        args: Parsed command-line arguments
    """
    try:
        task = _service.add(args.title, args.description)
        print("Task added successfully!")
        print(format_task_detail(task))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_list(args: Any) -> None:
    """Handle list command.

    Args:
        args: Parsed command-line arguments
    """
    tasks = _service.list_all()
    print(format_task_list(tasks))


def handle_update(args: Any) -> None:
    """Handle update command.

    Args:
        args: Parsed command-line arguments
    """
    # Validate that at least one field is provided
    if args.title is None and args.description is None:
        print("Error: Provide --title and/or --description", file=sys.stderr)
        sys.exit(2)

    try:
        task = _service.update(args.id, title=args.title, description=args.description)
        print("Task updated successfully!")
        print(format_task_detail(task))
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_delete(args: Any) -> None:
    """Handle delete command.

    Args:
        args: Parsed command-line arguments
    """
    try:
        _service.delete(args.id)
        print("Task deleted successfully!")
        print(f"ID: {args.id}")
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_complete(args: Any) -> None:
    """Handle complete command.

    Args:
        args: Parsed command-line arguments
    """
    try:
        task = _service.complete(args.id)
        print("Task marked as complete!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print("Status: ✓ Complete")
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_incomplete(args: Any) -> None:
    """Handle incomplete command.

    Args:
        args: Parsed command-line arguments
    """
    try:
        task = _service.uncomplete(args.id)
        print("Task marked as incomplete!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print("Status: ○ Incomplete")
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def execute_command(args: Any) -> None:
    """Execute the appropriate command based on parsed arguments.

    Args:
        args: Parsed command-line arguments
    """
    if args.command == "add":
        handle_add(args)
    elif args.command == "list":
        handle_list(args)
    elif args.command == "update":
        handle_update(args)
    elif args.command == "delete":
        handle_delete(args)
    elif args.command == "complete":
        handle_complete(args)
    elif args.command == "incomplete":
        handle_incomplete(args)
    else:
        print("Error: No command specified. Use --help for usage information.", file=sys.stderr)
        sys.exit(2)
