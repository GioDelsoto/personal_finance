from abc import ABC, abstractmethod
from src.schemas.messages.received_messages import ReceivedMessage
from src.schemas.messages.chat_messages import ChatMessage
from typing import List

class MessageProcessor(ABC):
    @abstractmethod
    def process_message(self, message: ReceivedMessage, chat_history: List[ChatMessage], user: dict) -> dict:
        ...

    @abstractmethod
    def _prepare_chat_history(self, chat_history: List[ChatMessage]) -> List[dict]:
        ...

    @abstractmethod
    def _get_system_prompt(self) -> str:
        ...