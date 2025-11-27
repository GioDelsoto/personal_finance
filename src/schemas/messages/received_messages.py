from pydantic import BaseModel, Field
from typing import Optional

class ReceivedMessage(BaseModel):
    media_url: Optional[str] = Field(None, description="URL to download the audio message")
    mime_type: Optional[str] = Field(None, description="MIME type of the audio message")
    text: Optional[str] = Field(None, description="Text message content")
    phone: str = Field(..., description="Sender phone number")
    message_id: str = Field(..., description="Received message ID")
