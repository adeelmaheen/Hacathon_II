"""Task API endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from src.api.deps import get_session, get_current_user
from src.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from src.services.task_service import TaskService

router = APIRouter()


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new todo task for the authenticated user"
)
def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task.

    - **title**: Task title (1-200 characters, required)
    - **description**: Optional task description (max 1000 characters)

    Returns the created task with auto-generated ID and timestamps.

    Requires authentication (JWT token in Authorization header or HTTPOnly cookie).
    """
    task = TaskService.create_task(session, user_id, task_data)
    return TaskResponse.model_validate(task)


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Get all tasks for authenticated user",
    description="Retrieve all tasks with optional filtering and sorting"
)
def get_tasks(
    status: Optional[str] = Query(None, description="Filter by status: 'all', 'pending', or 'completed'"),
    sort: str = Query("created", description="Sort by field: 'created' or 'title'"),
    order: str = Query("desc", description="Sort order: 'asc' or 'desc'"),
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> List[TaskResponse]:
    """
    Get all tasks for the authenticated user with filtering and sorting.

    Tasks are automatically filtered by user_id to ensure data isolation.

    Query Parameters:
        - status: Filter by completion status ('all', 'pending', 'completed'). Default: all tasks.
        - sort: Sort by field ('created', 'title'). Default: 'created'.
        - order: Sort order ('asc', 'desc'). Default: 'desc'.

    Requires authentication (JWT token in Authorization header or HTTPOnly cookie).

    Returns:
        List of tasks matching the filter criteria
    """
    tasks = TaskService.get_tasks(session, user_id, status=status, sort_by=sort, order=order)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.patch(
    "/{task_id}/toggle",
    response_model=TaskResponse,
    summary="Toggle task completion status",
    description="Toggle a task between completed and not completed"
)
def toggle_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Toggle task completion status.

    Flips the completed boolean: True → False or False → True.
    Updates the updated_at timestamp.

    Requires authentication and task ownership verification.

    Raises:
        404 Not Found: If task doesn't exist or doesn't belong to user
    """
    task = TaskService.toggle_task_completion(session, user_id, task_id)
    return TaskResponse.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update task title, description, and/or completion status"
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update a task's title, description, and/or completion status.

    Only provided fields will be updated. Omitted fields remain unchanged.
    Updates the updated_at timestamp.

    Requires authentication and task ownership verification.

    Raises:
        404 Not Found: If task doesn't exist or doesn't belong to user
        400 Bad Request: If validation fails (e.g., empty title)
    """
    task = TaskService.update_task(session, user_id, task_id, task_data)
    return TaskResponse.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Permanently delete a task"
)
def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a task permanently.

    Requires authentication and task ownership verification.

    Raises:
        404 Not Found: If task doesn't exist or doesn't belong to user

    Returns:
        204 No Content on successful deletion
    """
    TaskService.delete_task(session, user_id, task_id)
