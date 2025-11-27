from celery import shared_task
from typing import Dict, Any

from src.schemas.messages.received_messages import ReceivedMessage
from src.services.messages.process_message import MessageProcessor

@shared_task(name="process_message_task", bind = True, max_retries = 3)
def process_message_task(self, message_dict: Dict[str, any], session_id: str, user: Dict[str, Any]):
    try:
        message = ReceivedMessage(**message_dict)
        processor = MessageProcessor()
        return processor.process_message(message, session_id, user)
    except Exception as e:
        print("Error processing task process_message_task")

        try:
            raise self.retry(exc=e, countdown=2 ** self.request.retries)
        except self.MaxRetriesExceededError:
            print(f"Max retries exceeded for sending message to {message_dict.get('phone', 'unknown')}")
            return {
                "status": "error",
                "error": f"Failed to send message: {str(e)}"
            }