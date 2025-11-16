from FastAPI import Depends
from src.dependencies.messages import get_incoming_message_handler
from src.schemas.messages.receive_messages import ReceivedMessage

class MessagesController:
    def message_controller(self, message: ReceivedMessage, income_message_processor = Depends(get_incoming_message_handler)):

        user = retrieve_user(message.phone)
        if not user:
            return 'User not found', 404

        session = retrieve_or_create_session(user)

        income_message_processor.handle_incoming_message(message, session, user)
        
        return {"status": "message added to queue"}, 200