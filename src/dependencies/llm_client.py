from functools import lru_cache
from openai import OpenAI
from src.config.settings import Config

@lru_cache()
def get_openai_client() -> OpenAI:
    """
    Return a singleton instance of the OpenAI client.
    @lru_cache() ensures it is created only once.
    """
    return OpenAI(api_key=Config.OPENAI_API_KEY)
