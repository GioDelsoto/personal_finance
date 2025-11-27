import pytest
from unittest.mock import Mock, MagicMock, patch

from src.message_processors.processors import NormalChatProcessor


class TestNormalChatProcessor:
    
    def test_prepare_chat_history(self, sample_chat_history):
        # ARRANGE - Cria processor com client mockado manualmente
        processor = NormalChatProcessor.__new__(NormalChatProcessor)
        processor.client = MagicMock()
        
        # ACT
        prepared = processor._prepare_chat_history(sample_chat_history)
        
        # ASSERT
        assert prepared == [
            {"role": "user", "content": "Olá, preciso de ajuda com minhas finanças."},
            {"role": "assistant", "content": "Claro! Como posso ajudar você hoje?"}
        ]

    def test_get_system_prompt(self):
        # ARRANGE - Cria processor com client mockado manualmente
        processor = NormalChatProcessor.__new__(NormalChatProcessor)
        processor.client = MagicMock()
        
        # ACT
        prompt = processor._get_system_prompt()
        
        # ASSERT
        assert "financeiro" in prompt.lower()

    def test_process_message_success(self, sample_received_message, sample_chat_history, sample_user):
        # ARRANGE - Cria processor com client mockado manualmente
        processor = NormalChatProcessor.__new__(NormalChatProcessor)
        processor.client = MagicMock()
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Claro! Vamos começar organizando seu orçamento."
        processor.client.chat.completions.create.return_value = mock_response
        
        # ACT
        response = processor.process_message(sample_received_message, sample_chat_history, sample_user)
    
        # ASSERT
        assert response["status"] == "success"
        assert "response" in response
        assert response["response"] == "Claro! Vamos começar organizando seu orçamento."
        processor.client.chat.completions.create.assert_called_once()

    def test_process_message_failure(self, sample_received_message, sample_chat_history, sample_user):
        # ARRANGE - Cria processor com client mockado manualmente
        processor = NormalChatProcessor.__new__(NormalChatProcessor)
        processor.client = MagicMock()
        
        # Mock lança exceção
        processor.client.chat.completions.create.side_effect = Exception("API Error")

        # ACT
        result = processor.process_message(sample_received_message, sample_chat_history, sample_user)

        # ASSERT
        assert result["status"] == "error"
        assert "API Error" in result["response"]
        