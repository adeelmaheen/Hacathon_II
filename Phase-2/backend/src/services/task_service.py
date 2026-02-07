"""Task service for CRUD operations on tasks."""
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """
    Task service handling task CRUD operations with user isolation.

    All operations are scoped to the authenticated user to ensure
    data isolation and security.
    """

    @staticmethod
    def create_task(
        session: Session,
        user_id: str,
        task_data: TaskCreate
    ) -> Task:
        """
        Create a new task for the specified user.

        Args:
            session: Database session
            user_id: Authenticated user's UUID
            task_data: Task creation data (title, description)

        Returns:
            Created Task object with auto-generated ID and timestamps
        """
        # Create new task with user_id scoping
        new_task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Save to database
        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return new_task

    @staticmethod
    def get_tasks(
        session: Session,
        user_id: str,
        status: Optional[str] = None,
        sort_by: str = "created",
        order: str = "desc"
    ) -> List[Task]:
        """
        Get all tasks for the specified user with filtering and sorting.

        Args:
            session: Database session
            user_id: Authenticated user's UUID
            status: Filter by status ('all', 'pending', 'completed'). None or 'all' returns all tasks.
            sort_by: Sort field ('created' or 'title'). Defaults to 'created'.
            order: Sort order ('asc' or 'desc'). Defaults to 'desc'.

        Returns:
            List of Task objects belonging to the user
        """
        # Start with user_id filter
        statement = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status and status != "all":
            if status == "completed":
                statement = statement.where(Task.completed == True)
            elif status == "pending":
                statement = statement.where(Task.completed == False)

        # Apply sorting
        if sort_by == "title":
            sort_field = Task.title
        else:  # Default to created_at
            sort_field = Task.created_at

        if order == "asc":
            statement = statement.order_by(sort_field.asc())
        else:  # Default to desc
            statement = statement.order_by(sort_field.desc())

        tasks = session.exec(statement).all()
        return list(tasks)

    @staticmethod
    def toggle_task_completion(
        session: Session,
        user_id: str,
        task_id: int
    ) -> Task:
        """
        Toggle task completion status (completed ↔ not completed).

        Args:
            session: Database session
            user_id: Authenticated user's UUID
            task_id: Task ID to toggle

        Returns:
            Updated Task object

        Raises:
            HTTPException: 404 if task not found or doesn't belong to user
        """
        # Fetch task with user_id verification
        task = session.get(Task, task_id)

        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )

        # Toggle completion status
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def update_task(
        session: Session,
        user_id: str,
        task_id: int,
        task_data: TaskUpdate
    ) -> Task:
        """
        Update task title and/or description.

        Args:
            session: Database session
            user_id: Authenticated user's UUID
            task_id: Task ID to update
            task_data: Task update data (title, description, completed)

        Returns:
            Updated Task object

        Raises:
            HTTPException: 404 if task not found or doesn't belong to user
        """
        # Fetch task with user_id verification
        task = session.get(Task, task_id)

        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )

        # Update only provided fields
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Always update timestamp
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete_task(
        session: Session,
        user_id: str,
        task_id: int
    ) -> None:
        """
        Delete a task.

        Args:
            session: Database session
            user_id: Authenticated user's UUID
            task_id: Task ID to delete

        Raises:
            HTTPException: 404 if task not found or doesn't belong to user
        """
        # Fetch task with user_id verification
        task = session.get(Task, task_id)

        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )

        # Delete task
        session.delete(task)
        session.commit()
