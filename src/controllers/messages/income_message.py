from uuid import uuid4
from src.schemas.messages.received_messages import ReceivedMessage
from src.services.messages.income_message_handler import IncomingMessageHandler


class MessagesController:
    def __init__(self, income_message_handler: IncomingMessageHandler):
        # Recebe handler via dependency injection
        self.income_message_handler = income_message_handler
    
    def message_controller(self, message: ReceivedMessage):
        """
        Processa mensagem recebida:
        1. Busca/cria usuário (TODO)
        2. Busca/cria sessão (TODO)
        3. Enfileira mensagem para processamento assíncrono
        """
        # TODO: Implementar busca de usuário real
        # user = retrieve_user(message.phone)
        # if not user:
        #     raise HTTPException(status_code=404, detail="User not found")
        user = {"id": "temp-user", "name": "Temp User"}
        
        # TODO: Implementar sessão real
        # session = retrieve_or_create_session(user)
        session_id = uuid4()
        
        # Enfileira mensagem
        result = self.income_message_handler.handle_incoming_message(
            message, 
            session_id, 
            user
        )
        
        return result