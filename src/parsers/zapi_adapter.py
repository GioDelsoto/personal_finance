from src.schemas.messages.receive_messages import ReceivedMessage
from src.schemas.messages.received_messages_zapi import WhatsAppMessageZapi

class ZapiReceivedMessageAdapter:
    def parse_request(self, data: dict) -> ReceivedMessage:
        zapi_message = WhatsAppMessageZapi(**data)

        media_url = None
        mime_type = None
        text = None

        if zapi_message.audio:
            media_url = zapi_message.audio.audioUrl
            mime_type = zapi_message.audio.mimeType
        elif zapi_message.video:
            media_url = zapi_message.video.videoUrl
            mime_type = zapi_message.video.mimeType
        elif zapi_message.text:
            text = zapi_message.text.message

        return ReceivedMessage(
            media_url=media_url,
            mime_type=mime_type,
            text=text,
            phone=zapi_message.phone,
            message_id=zapi_message.message_id
        )