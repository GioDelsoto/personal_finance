from pydantic import BaseModel, Field
from typing import Optional


class MessageAudio(BaseModel):
    audioUrl: str = Field(..., description="URL to download the audio message")
    mimeType: str = Field(..., description="MIME type of the audio message")

class MessageVideo(BaseModel):
    videoUrl: str = Field(..., description="URL to download the video message")
    mimeType: str = Field(..., description="MIME type of the video message")

class MessageText(BaseModel):
    message: str = Field(..., description="Text message content")

class WhatsAppMessageZapi(BaseModel):
    phone: str = Field(..., description="Sender phone number")
    message_id: str = Field(..., description="Received message ID")
    audio: Optional[MessageAudio] = None
    text: Optional[MessageText] = None
    video: Optional[MessageVideo] = None