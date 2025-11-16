from functools import lru_cache
from src.parsers.interface_received_message_adapter import InterfaceReceivedMessageAdapter
from src.parsers.zapi_adapter import ZapiReceivedMessageAdapter
from src.services.messages.income_message_handler import IncomingMessageHandler

@lru_cache()
def get_message_parser() -> InterfaceReceivedMessageAdapter:
    return ZapiReceivedMessageAdapter()


@lru_cache()
def get_incoming_message_handler():
    return IncomingMessageHandler()