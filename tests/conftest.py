import pytest
from typing import Generator
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def app():
    """Cria a aplicação FastAPI para testes"""
    from main import app
    return app

@pytest.fixture
def client(app) -> Generator:
    """Cliente HTTP para testes de API"""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def sample_user():
    """Usuário de exemplo para testes"""
    return {
        "id": 1,
        "phone": "5511999999999",
        "name": "João Silva",
        "created_at": "2025-11-21T10:00:00"
    }

@pytest.fixture
def sample_session_id():
    """Session ID de exemplo para testes"""
    from uuid import uuid4
    return uuid4()


@pytest.fixture
def sample_received_message():
    """Mensagem de exemplo"""
    from src.schemas.messages.received_messages import ReceivedMessage
    return ReceivedMessage(
            text="Bom dia! Você pode me ajudar a organizar meu orçamento mensal?",
            phone="5511999999999",
            type="text",
            message_id="msg123",
        )

@pytest.fixture
def sample_chat_history():
    from src.schemas.messages.chat_messages import ChatMessage
    return [
        ChatMessage(role="user", content="Olá, preciso de ajuda com minhas finanças.", message_type="text", message_id="msg1", created_at="2024-01-01T10:00:00Z"),
        ChatMessage(role="assistant", content="Claro! Como posso ajudar você hoje?", message_type="text", message_id="msg2", created_at="2024-01-01T10:01:00Z")
    ]
    