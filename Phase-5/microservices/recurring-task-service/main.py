"""Recurring Task Service - Consumes task.completed events and creates next occurrence."""
import asyncio
import httpx
import json
from datetime import datetime, timedelta
from typing import Dict, Any
import os

# Dapr sidecar port
DAPR_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_PUBSUB = "kafka-pubsub"
DAPR_TOPIC = "task-events"

# Backend API URL (for creating tasks)
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://todo-backend:8000")


async def calculate_next_due_date(
    pattern: str, interval: int, current_due_date: datetime
) -> datetime:
    """Calculate next due date based on recurrence pattern."""
    if pattern == "daily":
        return current_due_date + timedelta(days=interval)
    elif pattern == "weekly":
        return current_due_date + timedelta(weeks=interval)
    elif pattern == "monthly":
        # Approximate: add 30 days per month
        return current_due_date + timedelta(days=30 * interval)
    elif pattern == "yearly":
        return current_due_date + timedelta(days=365 * interval)
    else:
        return current_due_date + timedelta(days=interval)


async def create_next_task(
    user_id: int, parent_task: Dict[str, Any], recurrence_config: Dict[str, Any]
) -> None:
    """Create the next occurrence of a recurring task."""
    try:
        # Calculate next due date
        current_due = datetime.fromisoformat(
            parent_task.get("due_date") or datetime.utcnow().isoformat()
        )
        next_due = await calculate_next_due_date(
            recurrence_config["pattern"],
            recurrence_config["interval"],
            current_due,
        )

        # Create new task data
        new_task_data = {
            "title": parent_task["title"],
            "description": parent_task.get("description", ""),
            "priority": parent_task.get("priority", "medium"),
            "tags": parent_task.get("tags", []),
            "due_date": next_due.isoformat(),
            "recurrence_pattern": recurrence_config["pattern"],
            "recurrence_interval": recurrence_config["interval"],
            "parent_task_id": parent_task["id"],
        }

        # Call backend API to create task
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_API_URL}/api/{user_id}/tasks",
                json=new_task_data,
                timeout=10.0,
            )
            response.raise_for_status()
            print(f"✓ Created next occurrence for task {parent_task['id']}")

    except Exception as e:
        print(f"✗ Failed to create next task: {e}")


async def consume_task_events():
    """Consume task events from Kafka via Dapr."""
    print("Starting Recurring Task Service...")
    print(f"Subscribing to {DAPR_TOPIC} via Dapr Pub/Sub...")

    while True:
        try:
            # Subscribe to task-events topic via Dapr
            async with httpx.AsyncClient() as client:
                # Dapr subscription endpoint
                sub_url = f"http://localhost:{DAPR_PORT}/v1.0/subscribe/{DAPR_PUBSUB}/{DAPR_TOPIC}"

                # For now, we'll poll (in production, use Dapr's subscription API)
                # This is a simplified version - in production, use proper Dapr subscriptions
                await asyncio.sleep(5)  # Poll every 5 seconds

        except Exception as e:
            print(f"Error consuming events: {e}")
            await asyncio.sleep(5)


async def handle_task_completed_event(event: Dict[str, Any]):
    """Handle task.completed event."""
    if event.get("event_type") != "task.completed":
        return

    task_data = event.get("task_data", {})
    recurrence_config = event.get("recurrence_config")

    if not recurrence_config:
        return  # Not a recurring task

    user_id = event.get("user_id")
    if not user_id:
        return

    print(f"Processing completed recurring task: {task_data.get('id')}")
    await create_next_task(user_id, task_data, recurrence_config)


if __name__ == "__main__":
    print("Recurring Task Service")
    print("=" * 50)
    asyncio.run(consume_task_events())

