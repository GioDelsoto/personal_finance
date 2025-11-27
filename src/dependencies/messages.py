from functools import lru_cache
from src.parsers.interface_received_message_adapter import InterfaceReceivedMessageAdapter
from src.parsers.zapi_adapter import ZapiReceivedMessageAdapter
from src.services.messages.income_message_handler import IncomingMessageHandler
from src.producers.queue_producer import QueueProducer


@lru_cache()
def get_message_parser() -> InterfaceReceivedMessageAdapter:
    return ZapiReceivedMessageAdapter()


@lru_cache()
def get_queue_producer() -> QueueProducer:
    return QueueProducer()


@lru_cache()
def get_incoming_message_handler():
    producer = get_queue_producer()
    return IncomingMessageHandler(producer=producer)


@lru_cache()
def get_messages_controller():
    from src.controllers.messages.income_message import MessagesController
    handler = get_incoming_message_handler()
    return MessagesController(income_message_handler=handler)

