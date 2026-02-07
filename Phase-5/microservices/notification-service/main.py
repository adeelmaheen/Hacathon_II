"""Notification Service - Consumes reminder events and sends notifications."""
import asyncio
import httpx
from datetime import datetime
from typing import Dict, Any
import os

# Dapr sidecar port
DAPR_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_PUBSUB = "kafka-pubsub"
DAPR_TOPIC = "reminders"


async def send_notification(reminder_data: Dict[str, Any]) -> None:
    """Send notification to user."""
    try:
        user_id = reminder_data.get("user_id")
        task_title = reminder_data.get("task_title", "Task")
        due_at = reminder_data.get("due_at")

        # In production, this would send email/push notification
        # For now, just log
        print(f"📧 Sending reminder to user {user_id}:")
        print(f"   Task: {task_title}")
        print(f"   Due: {due_at}")

        # TODO: Integrate with email service (SendGrid, AWS SES, etc.)
        # TODO: Integrate with push notification service (FCM, APNs, etc.)

    except Exception as e:
        print(f"✗ Failed to send notification: {e}")


async def consume_reminder_events():
    """Consume reminder events from Kafka via Dapr."""
    print("Starting Notification Service...")
    print(f"Subscribing to {DAPR_TOPIC} via Dapr Pub/Sub...")

    while True:
        try:
            # Subscribe to reminders topic via Dapr
            # In production, use Dapr's subscription API
            await asyncio.sleep(5)  # Poll every 5 seconds

        except Exception as e:
            print(f"Error consuming events: {e}")
            await asyncio.sleep(5)


async def handle_reminder_event(event: Dict[str, Any]):
    """Handle reminder event."""
    if event.get("event_type") != "reminder.scheduled":
        return

    remind_at = datetime.fromisoformat(event.get("remind_at"))
    now = datetime.utcnow()

    # Check if it's time to send reminder
    if remind_at <= now:
        await send_notification(event)


if __name__ == "__main__":
    print("Notification Service")
    print("=" * 50)
    asyncio.run(consume_reminder_events())

