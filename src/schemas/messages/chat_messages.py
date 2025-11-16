from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ChatMessage(BaseModel):
    message_type: str = Field(..., description="Type of the message, e.g., text, audio, video")
    text: Optional[str] = Field(None, description="Text message content")
    message_id: str = Field(..., description="Received message ID")
    role: str = Field(..., description="Role of the message sender, e.g., user, system")
    created_at: datetime = Field(..., description="Timestamp when the message was created") 
