from src.schemas.messages.received_messages import ReceivedMessage
from src.schemas.messages.chat_messages import ChatMessage
from uuid import UUID
from typing import Optional, List
from src.message_processors.processors import NormalChatProcessor, AddExpenseProcessor

class MessageProcessor:
    def __init__(self):
        pass

    def process_message(self, Message: ReceivedMessage, session_id: UUID, user: dict):
        
        #Recebe a mensagem
        #Pega o histórico da conversa
        chat_history = self.get_message_history(session_id)

        #Roteia a mensagem para o serviço apropriado
        message_route = self.get_message_route(Message, chat_history)
        #Registra a mensagem no banco de dados

        message_processor = self.factory_get_processor(message_route)

        message_processor.process_message(Message, chat_history, user)
        message_processor.save_message(Message, session_id, user)
        message_processor.update_chat_history_cache(session_id, Message)
        #Retorna uma resposta apropriada
        return {"status": "processed", "route": message_route}

    def get_message_history(self, session_id) -> List[ChatMessage]:
        """
        Retrieve the chat history for a given session ID.
        It looks if there are previous messages in cache. If not, it fetches from the database.
        Inputs:
            session_id: The unique identifier for the chat session.
        Returns:
            A list of ChatMessage objects representing the chat history.
        """

        return []
    
    def get_message_route(self, message: ReceivedMessage, chat_history: List[ChatMessage],) -> str:
        """
         Determine the route for the message based on its content and chat history. 
         Possible routes include: 
            - normal_chat: For standard user queries and interactions.
            - report_status: For requests related to financial report generation.
            - add_expense: For messages that involve adding new expenses.
            - analytics: For inquiries about financial analytics and insights.
            - unknown: If the message does not fit any known category.

            Inputs:
                message: The received message to be routed.
                chat_history: List of previous chat messages for context.
            Returns:
                A string indicating the determined route.
        """

        route = 'normal_chat'
        
        if route == 'normal_chat':
            return 'normal_chat'
        elif route == 'report_status':
            return 'report_status'
        elif route == 'add_expense':
            return 'add_expense'
        elif route == 'analytics':
            return 'analytics'
        else:
            return 'unknown'
        
    def factory_get_processor(self, route: str):
        """
        Factory method to get the appropriate message processor based on the route.
        Inputs:
            route: The determined route for the message.
        Returns:
            An instance of the appropriate message processor.
        """

        if route == 'normal_chat':
            return NormalChatProcessor()
        #elif route == 'report_status':
        #    return ReportStatusProcessor()
        elif route == 'add_expense':
            return AddExpenseProcessor()
        #elif route == 'analytics':
        #    return AnalyticsProcessor()
        else:
            return None #UnknownProcessor()
        
    def save_message(self, message: ReceivedMessage, session_id: UUID, user: dict):
        # TODO: Implement saving message to database
        pass

    def update_chat_history_cache(self, session_id: UUID, message: ReceivedMessage):
        # TODO: Implement updating chat history cache
        pass
