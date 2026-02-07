"""Task CRUD routes with advanced features."""
from fastapi import APIRouter, Depends, HTTPException, status, Header, Query, BackgroundTasks
from sqlmodel import Session, select, or_, and_
from typing import Optional, List, Literal, Annotated
from pydantic import BaseModel
from datetime import datetime
import json
from app.database import get_session
from app.models import Task, RecurringTask, Reminder
from app.auth import decode_token
from app.events import event_publisher

router = APIRouter(prefix="/api", tags=["tasks"])


class TaskCreate(BaseModel):
    """Task creation model with advanced features."""
    title: str
    description: str = ""
    priority: str = "medium"  # low, medium, high, urgent
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None  # daily, weekly, monthly, yearly, custom
    recurrence_interval: Optional[int] = None  # e.g., every 2 days


class TaskUpdate(BaseModel):
    """Task update model with advanced features."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None


class TaskResponse(BaseModel):
    """Task response model with advanced features."""
    id: int
    user_id: int
    title: str
    description: str
    completed: bool
    priority: Optional[str] = "medium"  # Optional with default for backward compatibility
    tags: Optional[str] = None  # JSON string
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None
    next_due_date: Optional[datetime] = None
    parent_task_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    """Extract user_id from JWT token."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    try:
        token = authorization.split(" ")[1]  # Remove "Bearer " prefix
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user_id"
        )
    
    return int(user_id)


def verify_user_access(user_id: int, token_user_id: int):
    """Verify that token user_id matches requested user_id."""
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch"
        )


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(
    user_id: int,
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """List all tasks for a user."""
    verify_user_access(user_id, token_user_id)
    
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: int,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Create a new task with advanced features."""
    verify_user_access(user_id, token_user_id)
    
    # Validate priority
    valid_priorities = ["low", "medium", "high", "urgent"]
    if task_data.priority not in valid_priorities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid priority. Must be one of: {valid_priorities}"
        )
    
    # Convert tags list to JSON string
    tags_json = json.dumps(task_data.tags) if task_data.tags else None
    
    new_task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        tags=tags_json,
        due_date=task_data.due_date,
        reminder_time=task_data.reminder_time,
        recurrence_pattern=task_data.recurrence_pattern,
        recurrence_interval=task_data.recurrence_interval,
        next_due_date=task_data.due_date if task_data.recurrence_pattern else None
    )
    
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    
    # Create recurring task record if recurrence is set
    if task_data.recurrence_pattern:
        recurring_task = RecurringTask(
            task_id=new_task.id,
            pattern=task_data.recurrence_pattern,
            interval=task_data.recurrence_interval or 1,
            next_due_date=task_data.due_date
        )
        session.add(recurring_task)
        session.commit()
    
    # Create reminder if reminder_time is set
    if task_data.reminder_time:
        reminder = Reminder(
            task_id=new_task.id,
            user_id=user_id,
            remind_at=task_data.reminder_time
        )
        session.add(reminder)
        session.commit()
        
        # Publish reminder event
        await event_publisher.publish_reminder_event(
            task_id=new_task.id,
            user_id=user_id,
            task_title=new_task.title,
            due_at=task_data.due_date or datetime.utcnow(),
            remind_at=task_data.reminder_time
        )
    
    # Publish task created event
    task_dict = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "priority": new_task.priority,
        "tags": json.loads(new_task.tags) if new_task.tags else [],
        "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
        "recurrence_pattern": new_task.recurrence_pattern,
    }
    
    recurrence_config = None
    if task_data.recurrence_pattern:
        recurrence_config = {
            "pattern": task_data.recurrence_pattern,
            "interval": task_data.recurrence_interval or 1,
            "next_due_date": task_data.due_date.isoformat() if task_data.due_date else None
        }
    
    await event_publisher.publish_task_event(
        event_type="task.created",
        task_id=new_task.id,
        user_id=user_id,
        task_data=task_dict,
        recurrence_config=recurrence_config
    )
    
    return new_task


# IMPORTANT: Specific routes (like /combined, /search, /filter, /sort) must come BEFORE
# parameterized routes (like /{task_id}) to avoid route conflicts
@router.get("/{user_id}/tasks/search", response_model=List[TaskResponse])
async def search_tasks(
    user_id: int,
    q: str = Query(..., description="Search query"),
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Search tasks by title or description."""
    verify_user_access(user_id, token_user_id)
    
    # Full-text search on title and description
    statement = select(Task).where(
        and_(
            Task.user_id == user_id,
            or_(
                Task.title.ilike(f"%{q}%"),
                Task.description.ilike(f"%{q}%")
            )
        )
    )
    tasks = session.exec(statement).all()
    
    return tasks


@router.get("/{user_id}/tasks/filter", response_model=List[TaskResponse])
async def filter_tasks(
    user_id: int,
    status: Optional[str] = Query(None, description="Filter by status: completed, pending, all"),
    priority: Optional[str] = Query(None, description="Filter by priority: low, medium, high, urgent"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    due_before: Optional[datetime] = Query(None, description="Filter tasks due before this date"),
    due_after: Optional[datetime] = Query(None, description="Filter tasks due after this date"),
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Filter tasks by various criteria."""
    verify_user_access(user_id, token_user_id)
    
    statement = select(Task).where(Task.user_id == user_id)
    
    # Filter by status
    if status == "completed":
        statement = statement.where(Task.completed == True)
    elif status == "pending":
        statement = statement.where(Task.completed == False)
    
    # Filter by priority
    if priority:
        statement = statement.where(Task.priority == priority)
    
    # Filter by tag
    if tag:
        statement = statement.where(Task.tags.contains(f'"{tag}"'))
    
    # Filter by due date range
    if due_after:
        statement = statement.where(Task.due_date >= due_after)
    if due_before:
        statement = statement.where(Task.due_date <= due_before)
    
    tasks = session.exec(statement).all()
    
    return tasks


@router.get("/{user_id}/tasks/sort", response_model=List[TaskResponse])
async def sort_tasks(
    user_id: int,
    sort_by: str = Query("created_at", description="Sort by: created_at, due_date, priority, title"),
    order: str = Query("desc", description="Sort order: asc, desc"),
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Sort tasks by various fields."""
    verify_user_access(user_id, token_user_id)
    
    statement = select(Task).where(Task.user_id == user_id)
    
    # Map sort_by to model fields
    sort_fields = {
        "created_at": Task.created_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
        "title": Task.title
    }
    
    # Validate sort_by
    if sort_by not in sort_fields:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid sort_by. Must be one of: {list(sort_fields.keys())}"
        )
    
    # Validate order
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid order. Must be 'asc' or 'desc'"
        )
    
    # Apply sorting
    if order == "asc":
        statement = statement.order_by(sort_fields[sort_by])
    else:
        statement = statement.order_by(sort_fields[sort_by].desc())
    
    tasks = session.exec(statement).all()
    
    return tasks


@router.get("/{user_id}/tasks/combined", response_model=List[TaskResponse])
async def search_filter_sort_tasks(
    user_id: int,
    q: Optional[str] = Query(None, description="Search query"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    sort_by: Optional[str] = Query("created_at", description="Sort by field: created_at, due_date, priority, title"),
    order: Optional[str] = Query("desc", description="Sort order: asc, desc"),
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Combined search, filter, and sort endpoint."""
    verify_user_access(user_id, token_user_id)
    
    # Set defaults if None
    sort_by = sort_by or "created_at"
    order = order or "desc"
    
    # Validate sort_by
    valid_sort_fields = ["created_at", "due_date", "priority", "title"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid sort_by. Must be one of: {valid_sort_fields}"
        )
    
    # Validate order
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid order. Must be 'asc' or 'desc'"
        )
    
    statement = select(Task).where(Task.user_id == user_id)
    
    # Apply search
    if q:
        statement = statement.where(
            or_(
                Task.title.ilike(f"%{q}%"),
                Task.description.ilike(f"%{q}%")
            )
        )
    
    # Apply filters
    if status == "completed":
        statement = statement.where(Task.completed == True)
    elif status == "pending":
        statement = statement.where(Task.completed == False)
    
    if priority:
        statement = statement.where(Task.priority == priority)
    
    if tag:
        statement = statement.where(Task.tags.contains(f'"{tag}"'))
    
    # Apply sorting
    sort_fields = {
        "created_at": Task.created_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
        "title": Task.title
    }
    
    if sort_by in sort_fields:
        if order == "asc":
            statement = statement.order_by(sort_fields[sort_by])
        else:
            statement = statement.order_by(sort_fields[sort_by].desc())
    
    tasks = session.exec(statement).all()
    
    # Convert to TaskResponse to ensure proper serialization
    # Handle None values and ensure all required fields are present
    task_responses = []
    for task in tasks:
        try:
            # Ensure priority has a default value if None
            priority_value = task.priority if task.priority else "medium"
            
            task_response = TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description or "",
                completed=task.completed,
                priority=priority_value,
                tags=task.tags,
                due_date=task.due_date,
                reminder_time=task.reminder_time,
                recurrence_pattern=task.recurrence_pattern,
                recurrence_interval=task.recurrence_interval,
                next_due_date=task.next_due_date,
                parent_task_id=task.parent_task_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            task_responses.append(task_response)
        except Exception as e:
            # Log error but continue with other tasks
            print(f"Error serializing task {task.id}: {e}")
            continue
    
    return task_responses


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Get a specific task."""
    verify_user_access(user_id, token_user_id)
    
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: int,
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Update a task."""
    verify_user_access(user_id, token_user_id)
    
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
    if task_data.priority is not None:
        valid_priorities = ["low", "medium", "high", "urgent"]
        if task_data.priority not in valid_priorities:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid priority. Must be one of: {valid_priorities}"
            )
        task.priority = task_data.priority
    if task_data.tags is not None:
        task.tags = json.dumps(task_data.tags) if task_data.tags else None
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.reminder_time is not None:
        task.reminder_time = task_data.reminder_time
        # Update or create reminder
        existing_reminder = session.exec(
            select(Reminder).where(Reminder.task_id == task_id)
        ).first()
        if existing_reminder:
            existing_reminder.remind_at = task_data.reminder_time
            existing_reminder.sent = False
        else:
            reminder = Reminder(
                task_id=task_id,
                user_id=user_id,
                remind_at=task_data.reminder_time
            )
            session.add(reminder)
    if task_data.recurrence_pattern is not None:
        task.recurrence_pattern = task_data.recurrence_pattern
        task.recurrence_interval = task_data.recurrence_interval or 1
        task.next_due_date = task_data.due_date if task_data.due_date else task.next_due_date
    
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Delete a task and its related records."""
    verify_user_access(user_id, token_user_id)
    
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Delete related records first to avoid foreign key constraint violations
    # Delete recurring task records
    recurring_tasks = session.exec(
        select(RecurringTask).where(RecurringTask.task_id == task_id)
    ).all()
    for rt in recurring_tasks:
        session.delete(rt)
    
    # Delete reminder records
    reminders = session.exec(
        select(Reminder).where(Reminder.task_id == task_id)
    ).all()
    for reminder in reminders:
        session.delete(reminder)
    
    # Commit related deletions first
    session.commit()
    
    # Publish task deleted event before deletion
    try:
        await event_publisher.publish_task_event(
            event_type="task.deleted",
            task_id=task_id,
            user_id=user_id,
            task_data={"id": task.id, "title": task.title}
        )
    except Exception as e:
        # Log error but continue with deletion
        print(f"Failed to publish delete event: {e}")
    
    # Now delete the task itself
    session.delete(task)
    session.commit()
    
    return None


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Toggle task completion status."""
    verify_user_access(user_id, token_user_id)
    
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    # Publish task completed event (for recurring tasks)
    if task.completed:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "tags": json.loads(task.tags) if task.tags else [],
            "recurrence_pattern": task.recurrence_pattern,
            "recurrence_interval": task.recurrence_interval,
            "next_due_date": task.next_due_date.isoformat() if task.next_due_date else None,
        }
        
        recurrence_config = None
        if task.recurrence_pattern:
            recurrence_config = {
                "pattern": task.recurrence_pattern,
                "interval": task.recurrence_interval or 1,
                "next_due_date": task.next_due_date.isoformat() if task.next_due_date else None
            }
        
        await event_publisher.publish_task_event(
            event_type="task.completed",
            task_id=task.id,
            user_id=user_id,
            task_data=task_dict,
            recurrence_config=recurrence_config
        )
    
    return task


@router.get("/{user_id}/tasks/search", response_model=List[TaskResponse])
async def search_tasks(
    user_id: int,
    q: str = Query(..., description="Search query"),
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Search tasks by title or description."""
    verify_user_access(user_id, token_user_id)
    
    # Full-text search on title and description
    statement = select(Task).where(
        and_(
            Task.user_id == user_id,
            or_(
                Task.title.ilike(f"%{q}%"),
                Task.description.ilike(f"%{q}%")
            )
        )
    )
    tasks = session.exec(statement).all()
    
    return tasks


@router.get("/{user_id}/tasks/filter", response_model=List[TaskResponse])
async def filter_tasks(
    user_id: int,
    status: Optional[str] = Query(None, description="Filter by status: completed, pending, all"),
    priority: Optional[str] = Query(None, description="Filter by priority: low, medium, high, urgent"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    due_before: Optional[datetime] = Query(None, description="Filter tasks due before this date"),
    due_after: Optional[datetime] = Query(None, description="Filter tasks due after this date"),
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Filter tasks by various criteria."""
    verify_user_access(user_id, token_user_id)
    
    statement = select(Task).where(Task.user_id == user_id)
    
    # Filter by status
    if status == "completed":
        statement = statement.where(Task.completed == True)
    elif status == "pending":
        statement = statement.where(Task.completed == False)
    
    # Filter by priority
    if priority:
        statement = statement.where(Task.priority == priority)
    
    # Filter by tag
    if tag:
        statement = statement.where(Task.tags.contains(f'"{tag}"'))
    
    # Filter by due date range
    if due_after:
        statement = statement.where(Task.due_date >= due_after)
    if due_before:
        statement = statement.where(Task.due_date <= due_before)
    
    tasks = session.exec(statement).all()
    
    return tasks


@router.get("/{user_id}/tasks/sort", response_model=List[TaskResponse])
async def sort_tasks(
    user_id: int,
    sort_by: str = Query("created_at", description="Sort by: created_at, due_date, priority, title"),
    order: str = Query("desc", description="Sort order: asc, desc"),
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Sort tasks by various fields."""
    verify_user_access(user_id, token_user_id)
    
    statement = select(Task).where(Task.user_id == user_id)
    
    # Map sort_by to model fields
    sort_fields = {
        "created_at": Task.created_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
        "title": Task.title
    }
    
    # Validate sort_by
    if sort_by not in sort_fields:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid sort_by. Must be one of: {list(sort_fields.keys())}"
        )
    
    # Validate order
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid order. Must be 'asc' or 'desc'"
        )
    
    # Apply sorting
    if order == "asc":
        statement = statement.order_by(sort_fields[sort_by])
    else:
        statement = statement.order_by(sort_fields[sort_by].desc())
    
    tasks = session.exec(statement).all()
    
    return tasks


@router.get("/{user_id}/tasks/combined", response_model=List[TaskResponse])
async def search_filter_sort_tasks(
    user_id: int,
    q: Optional[str] = Query(None, description="Search query"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    sort_by: Optional[str] = Query("created_at", description="Sort by field: created_at, due_date, priority, title"),
    order: Optional[str] = Query("desc", description="Sort order: asc, desc"),
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Combined search, filter, and sort endpoint."""
    verify_user_access(user_id, token_user_id)
    
    # Set defaults if None
    sort_by = sort_by or "created_at"
    order = order or "desc"
    
    # Validate sort_by
    valid_sort_fields = ["created_at", "due_date", "priority", "title"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid sort_by. Must be one of: {valid_sort_fields}"
        )
    
    # Validate order
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid order. Must be 'asc' or 'desc'"
        )
    
    statement = select(Task).where(Task.user_id == user_id)
    
    # Apply search
    if q:
        statement = statement.where(
            or_(
                Task.title.ilike(f"%{q}%"),
                Task.description.ilike(f"%{q}%")
            )
        )
    
    # Apply filters
    if status == "completed":
        statement = statement.where(Task.completed == True)
    elif status == "pending":
        statement = statement.where(Task.completed == False)
    
    if priority:
        statement = statement.where(Task.priority == priority)
    
    if tag:
        statement = statement.where(Task.tags.contains(f'"{tag}"'))
    
    # Apply sorting
    sort_fields = {
        "created_at": Task.created_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
        "title": Task.title
    }
    
    if sort_by in sort_fields:
        if order == "asc":
            statement = statement.order_by(sort_fields[sort_by])
        else:
            statement = statement.order_by(sort_fields[sort_by].desc())
    
    tasks = session.exec(statement).all()
    
    # Convert to TaskResponse to ensure proper serialization
    # Handle None values and ensure all required fields are present
    task_responses = []
    for task in tasks:
        try:
            # Ensure priority has a default value if None
            priority_value = task.priority if task.priority else "medium"
            
            task_response = TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description or "",
                completed=task.completed,
                priority=priority_value,
                tags=task.tags,
                due_date=task.due_date,
                reminder_time=task.reminder_time,
                recurrence_pattern=task.recurrence_pattern,
                recurrence_interval=task.recurrence_interval,
                next_due_date=task.next_due_date,
                parent_task_id=task.parent_task_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            task_responses.append(task_response)
        except Exception as e:
            # Log error but continue with other tasks
            print(f"Error serializing task {task.id}: {e}")
            continue
    
    return task_responses

