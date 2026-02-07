"""Main entry point for Todo CLI application."""

import sys
from src.services.task_service import TaskService
from src.models.exceptions import TaskNotFoundError
from src.cli.formatter import format_task_list, format_task_detail


def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("TODO CLI - Main Menu")
    print("=" * 50)
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Mark task as complete")
    print("4. Mark task as incomplete")
    print("5. Update task")
    print("6. Delete task")
    print("7. Exit")
    print("=" * 50)


def handle_add(service: TaskService) -> None:
    """Handle adding a new task interactively."""
    print("\n--- Add New Task ---")
    title = input("Enter task title: ").strip()

    if not title:
        print("Error: Title cannot be empty!")
        return

    description = input("Enter task description (optional, press Enter to skip): ").strip()

    try:
        task = service.add(title, description)
        print("\nTask added successfully!")
        print(format_task_detail(task))
    except ValueError as e:
        print(f"Error: {e}")


def handle_view(service: TaskService) -> None:
    """Handle viewing all tasks."""
    print("\n--- All Tasks ---")
    tasks = service.list_all()
    print(format_task_list(tasks))


def handle_complete(service: TaskService) -> None:
    """Handle marking a task as complete."""
    print("\n--- Mark Task as Complete ---")
    try:
        task_id = int(input("Enter task ID: "))
        task = service.complete(task_id)
        print("\nTask marked as complete!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print("Status: [X] Complete")
    except ValueError:
        print("Error: Invalid task ID. Please enter a number.")
    except TaskNotFoundError as e:
        print(f"Error: {e}")


def handle_incomplete(service: TaskService) -> None:
    """Handle marking a task as incomplete."""
    print("\n--- Mark Task as Incomplete ---")
    try:
        task_id = int(input("Enter task ID: "))
        task = service.uncomplete(task_id)
        print("\nTask marked as incomplete!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print("Status: [ ] Incomplete")
    except ValueError:
        print("Error: Invalid task ID. Please enter a number.")
    except TaskNotFoundError as e:
        print(f"Error: {e}")


def handle_update(service: TaskService) -> None:
    """Handle updating a task."""
    print("\n--- Update Task ---")
    try:
        task_id = int(input("Enter task ID: "))

        # Show current task
        current_task = service.get(task_id)
        print("\nCurrent task:")
        print(format_task_detail(current_task))

        print("\nEnter new values (press Enter to keep current value):")
        new_title = input(f"New title [{current_task.title}]: ").strip()
        new_description = input(f"New description [{current_task.description}]: ").strip()

        # Only update if user provided new values
        title = new_title if new_title else None
        description = new_description if new_description else None

        if title is None and description is None:
            print("No changes made.")
            return

        task = service.update(task_id, title=title, description=description)
        print("\nTask updated successfully!")
        print(format_task_detail(task))

    except ValueError:
        print("Error: Invalid task ID. Please enter a number.")
    except TaskNotFoundError as e:
        print(f"Error: {e}")


def handle_delete(service: TaskService) -> None:
    """Handle deleting a task."""
    print("\n--- Delete Task ---")
    try:
        task_id = int(input("Enter task ID: "))

        # Show task before deleting
        task = service.get(task_id)
        print("\nTask to delete:")
        print(format_task_detail(task))

        confirm = input("\nAre you sure you want to delete this task? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            service.delete(task_id)
            print("\nTask deleted successfully!")
            print(f"ID: {task_id}")
        else:
            print("Delete cancelled.")

    except ValueError:
        print("Error: Invalid task ID. Please enter a number.")
    except TaskNotFoundError as e:
        print(f"Error: {e}")


def run_interactive_mode() -> int:
    """Run the application in interactive mode.

    Returns:
        Exit code (0 for success)
    """
    # Create a single service instance that persists for the session
    service = TaskService()

    # Display welcome message
    print("\n" + "=" * 50)
    print("Welcome to TODO CLI!")
    print("=" * 50)
    print("\nNote: All tasks are stored in memory.")
    print("Data will be lost when you exit the application.")

    # Main application loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            handle_add(service)
        elif choice == "2":
            handle_view(service)
        elif choice == "3":
            handle_complete(service)
        elif choice == "4":
            handle_incomplete(service)
        elif choice == "5":
            handle_update(service)
        elif choice == "6":
            handle_delete(service)
        elif choice == "7":
            print("\nThank you for using TODO CLI!")
            print("Exiting... All tasks will be lost.")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 7.")

        # Pause before showing menu again
        input("\nPress Enter to continue...")

    return 0


def main() -> int:
    """Run the todo CLI application.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        return run_interactive_mode()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        print("Exiting... All tasks will be lost.")
        return 0
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
