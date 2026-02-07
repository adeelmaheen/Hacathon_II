"""MCP Tools for task management."""
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task, User
from typing import Dict, Any, List, Optional
import asyncio


async def add_task(
    user_id: str,
    title: str,
    description: str = "",
    session: Session = None
) -> Dict[str, Any]:
    """
    Create a new task for the user.
    
    Args:
        user_id: User identifier (as string, will be converted to int)
        title: Task title (required)
        description: Task description (optional)
        session: Database session (required - must be passed from chat endpoint)
    
    Returns:
        Dict with task_id, status, and title
    """
    try:
        if session is None:
            return {
                "status": "error",
                "message": "Database session is required"
            }
        
        user_id_int = int(user_id)
        
        new_task = Task(
            user_id=user_id_int,
            title=title,
            description=description or ""
        )
        
        session.add(new_task)
        session.flush()  # Flush to get the ID without committing - makes it visible in same transaction
        session.refresh(new_task)
        
        # Verify the task was actually created
        if new_task.id is None:
            return {
                "status": "error",
                "message": "Failed to create task - no ID assigned"
            }
        
        return {
            "task_id": new_task.id,
            "status": "success",
            "title": new_task.title,
            "message": f"Task '{title}' created successfully"
        }
    except Exception as e:
        session.rollback()
        return {
            "status": "error",
            "message": f"Failed to create task: {str(e)}"
        }


async def list_tasks(
    user_id: str,
    status: str = "all",
    session: Session = None
) -> Dict[str, Any]:
    """
    List tasks for a user.
    
    Args:
        user_id: User identifier (as string)
        status: Filter by status - "all", "pending", or "completed"
        session: Database session (required - must be passed from chat endpoint)
    
    Returns:
        Dict with status and list of tasks
    """
    try:
        if session is None:
            return {
                "status": "error",
                "message": "Database session is required"
            }
        
        user_id_int = int(user_id)
        
        # Expire all to ensure we see the latest data including flushed changes
        session.expire_all()
        
        statement = select(Task).where(Task.user_id == user_id_int)
        
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)
        
        tasks = session.exec(statement.order_by(Task.created_at.desc())).all()
        
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]
        
        return {
            "status": "success",
            "count": len(task_list),
            "tasks": task_list,
            "message": f"Found {len(task_list)} task(s)"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list tasks: {str(e)}"
        }


async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    session: Session = None
) -> Dict[str, Any]:
    """
    Update task details.
    
    Args:
        user_id: User identifier (as string)
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)
        session: Database session (required - must be passed from chat endpoint)
    
    Returns:
        Dict with task_id, status, and title
    """
    try:
        if session is None:
            return {
                "status": "error",
                "message": "Database session is required"
            }
        
        user_id_int = int(user_id)
        
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id_int
        )
        task = session.exec(statement).first()
        
        if not task:
            return {
                "status": "error",
                "message": f"Task {task_id} not found"
            }
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        
        from datetime import datetime
        task.updated_at = datetime.utcnow()
        
        session.add(task)
        session.flush()
        session.refresh(task)
        
        return {
            "task_id": task.id,
            "status": "success",
            "title": task.title,
            "message": f"Task '{task.title}' updated successfully"
        }
    except Exception as e:
        session.rollback()
        return {
            "status": "error",
            "message": f"Failed to update task: {str(e)}"
        }


async def delete_task(
    user_id: str,
    task_id: int,
    session: Session = None
) -> Dict[str, Any]:
    """
    Delete a task.
    
    Args:
        user_id: User identifier (as string)
        task_id: Task ID to delete
        session: Database session (required - must be passed from chat endpoint)
    
    Returns:
        Dict with task_id and status
    """
    try:
        if session is None:
            return {
                "status": "error",
                "message": "Database session is required"
            }
        
        user_id_int = int(user_id)
        
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id_int
        )
        task = session.exec(statement).first()
        
        if not task:
            return {
                "status": "error",
                "message": f"Task {task_id} not found"
            }
        
        task_title = task.title
        session.delete(task)
        session.flush()
        
        return {
            "task_id": task_id,
            "status": "success",
            "message": f"Task '{task_title}' deleted successfully"
        }
    except Exception as e:
        session.rollback()
        return {
            "status": "error",
            "message": f"Failed to delete task: {str(e)}"
        }


async def complete_task(
    user_id: str,
    task_id: int,
    session: Session = None
) -> Dict[str, Any]:
    """
    Toggle task completion status.
    
    Args:
        user_id: User identifier (as string)
        task_id: Task ID to toggle
        session: Database session (required - must be passed from chat endpoint)
    
    Returns:
        Dict with task_id, status, and completed flag
    """
    try:
        if session is None:
            return {
                "status": "error",
                "message": "Database session is required"
            }
        
        user_id_int = int(user_id)
        
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id_int
        )
        task = session.exec(statement).first()
        
        if not task:
            return {
                "status": "error",
                "message": f"Task {task_id} not found"
            }
        
        task.completed = not task.completed
        from datetime import datetime
        task.updated_at = datetime.utcnow()
        
        session.add(task)
        session.flush()
        session.refresh(task)
        
        status_text = "completed" if task.completed else "marked as pending"
        
        return {
            "task_id": task.id,
            "status": "success",
            "completed": task.completed,
            "title": task.title,
            "message": f"Task '{task.title}' {status_text}"
        }
    except Exception as e:
        session.rollback()
        return {
            "status": "error",
            "message": f"Failed to toggle task: {str(e)}"
        }

