from fastapi import Depends
from src.schemas.messages.received_messages import ReceivedMessage
from src.producers.interface_queue_producer import InterfaceQueueProducer
from src.tasks.messages.process_message_task import process_message_task
from uuid import UUID


class IncomingMessageHandler:
    def __init__(self, producer: InterfaceQueueProducer, repository=None):
        self.repository = repository
        self.producer = producer

    def handle_incoming_message(self, message: ReceivedMessage, session_id: UUID, user: dict):
        """
        Handle an incoming message by saving it and enqueuing it for processing.
        """
        # Save message to repository (if needed)
        # self.repository.save_received_message(message, session_id, user)
        
        # Enqueue task for async processing
        message_dict = message.model_dump()
        user_dict = user if isinstance(user, dict) else {"id": str(user.id), "name": user.name}
        
        self.producer.enqueue(
            process_message_task,
            message_dict=message_dict,
            session_id=str(session_id),
            user=user_dict
        )
        
        return {"status": "queued", "message_id": message.message_id}

    