from typing import Protocol
from src.schemas.messages.receive_messages import ReceivedMessage

class InterfaceReceivedMessageAdapter(Protocol):
    """Interface for parsing received messages from different WhatsApp API providers."""
    def parse_request(self, data: any) -> ReceivedMessage:
        ...