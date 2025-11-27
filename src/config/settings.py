import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # Z-Api WhatsApp - Updated structure
    ZAPI_ENDPOINT_TEXT = os.getenv('ZAPI_ENDPOINT_TEXT', '')
    ZAPI_TOKEN = os.getenv('ZAPI_TOKEN', '')

    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

    # Google Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

    # ElevenLabs
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')
    ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', '')
    
    # Celery / Redis
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    # Session/Cookie
    SESSION_COOKIE_LIFETIME = int(os.getenv('SESSION_COOKIE_LIFETIME', 86400))  # 1 day default
