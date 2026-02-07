"""Event publishing utilities for Kafka integration."""
from typing import Dict, Any, Optional
from datetime import datetime
import json
import httpx
from app.config import settings


class EventPublisher:
    """Publish events to Kafka via Dapr Pub/Sub."""
    
    def __init__(self):
        self.dapr_port = 3500  # Default Dapr sidecar port
        self.pubsub_name = "kafka-pubsub"  # Dapr Pub/Sub component name
    
    async def publish_task_event(
        self,
        event_type: str,
        task_id: int,
        user_id: int,
        task_data: Optional[Dict[str, Any]] = None,
        recurrence_config: Optional[Dict[str, Any]] = None
    ):
        """Publish a task event to Kafka."""
        event = {
            "event_type": event_type,
            "task_id": task_id,
            "user_id": user_id,
            "task_data": task_data or {},
            "recurrence_config": recurrence_config,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        topic = "task-events"
        return await self._publish(topic, event)
    
    async def publish_reminder_event(
        self,
        task_id: int,
        user_id: int,
        task_title: str,
        due_at: datetime,
        remind_at: datetime
    ):
        """Publish a reminder event to Kafka."""
        event = {
            "event_type": "reminder.scheduled",
            "task_id": task_id,
            "user_id": user_id,
            "task_title": task_title,
            "due_at": due_at.isoformat(),
            "remind_at": remind_at.isoformat(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        topic = "reminders"
        return await self._publish(topic, event)
    
    async def publish_task_update_event(
        self,
        task_id: int,
        user_id: int,
        update_data: Dict[str, Any]
    ):
        """Publish a task update event for real-time sync."""
        event = {
            "event_type": "task.updated",
            "task_id": task_id,
            "user_id": user_id,
            "update_data": update_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        topic = "task-updates"
        return await self._publish(topic, event)
    
    async def _publish(self, topic: str, event: Dict[str, Any]) -> bool:
        """Publish event via Dapr Pub/Sub."""
        try:
            url = f"http://localhost:{self.dapr_port}/v1.0/publish/{self.pubsub_name}/{topic}"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=event, timeout=5.0)
                response.raise_for_status()
                return True
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to publish event to {topic}: {e}")
            return False


# Global event publisher instance
event_publisher = EventPublisher()

