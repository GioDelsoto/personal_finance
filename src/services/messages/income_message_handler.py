from FastAPI import Depends
from src.schemas.messages.receive_messages import ReceivedMessage
from uuid import UUID

class IncomingMessageHandler:
    def __init__(self, ):
        repository = None # Placeholder for message repository
        producer = None # Placeholder for message queue producer


    def handle_incoming_message(self, message: ReceivedMessage, session_id: UUID, user: dict):
        """
        Handle an incoming message by saving it and enqueuing it for processing.
        """
        self.repository.save_received_message(message, session_id, user)
        self.producer.enqueue_message_for_processing(message, session_id, user)
        return {"status": "queued"}

    