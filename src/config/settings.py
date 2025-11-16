import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    SUPABASE_API_KEY = os.getenv('SUPABASE_API_KEY', '')

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

    # Session/Cookie
    SESSION_COOKIE_LIFETIME = int(os.getenv('SESSION_COOKIE_LIFETIME', 86400))  # 1 day default
