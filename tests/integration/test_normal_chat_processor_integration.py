import pytest
import os
from src.message_processors.processors import NormalChatProcessor
from src.schemas.messages.received_messages import ReceivedMessage
from src.schemas.messages.chat_messages import ChatMessage


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not configured - skip integration tests"
)
class TestNormalChatProcessorIntegration:
    """
    Integration tests - calls real OpenAI API!
    
    IMPORTANT:
    - These tests make real calls to OpenAI API
    - Cost money (cents per call)
    - Require OPENAI_API_KEY configured
    - Are slower than unit tests
    
    To run:
        pytest tests/integration/ -v -m integration
    
    To skip:
        pytest tests/ -v -m "not integration"
    """
    
    @pytest.fixture
    def processor(self):
        """Creates REAL processor (no mock)"""
        return NormalChatProcessor()
    
    def test_process_message_real_api_no_history(self, processor, sample_received_message, sample_user):
        """
        Integration test: Calls real OpenAI API without history
        
        Verifies:
        - API responds
        - Response has correct format
        - Content is relevant
        """
        # ACT
        result = processor.process_message(
            message=sample_received_message,
            chat_history=[],
            user=sample_user
        )
        
        # ASSERT - Estrutura
        assert result is not None
        assert "status" in result
        assert "response" in result
        assert result["status"] == "success"
        
        # ASSERT - Conteúdo
        assert isinstance(result["response"], str)
        assert len(result["response"]) > 0

    def test_process_message_real_api_with_history(self, processor, sample_chat_history, sample_user):
        """
        Integration test: Calls OpenAI with conversation history
        
        Verifies:
        - API maintains conversation context
        - Response is coherent with history
        """
        
        # Mensagem que referencia o histórico
        followup_message = ReceivedMessage(
            text="Gasto R$ 2000 com aluguel e R$ 500 com alimentação",
            phone="5511999999999",
            message_id="integration_test_002"
        )
        
        # ACT
        result = processor.process_message(
            message=followup_message,
            chat_history=sample_chat_history,
            user=sample_user
        )
        
        # ASSERT
        assert result["status"] == "success"
        assert len(result["response"]) > 0
        
        # Verifica que resposta é contextual
        response_lower = result["response"].lower()
        has_context = any(word in response_lower for word in 
            ["2000", "500", "aluguel", "alimentação", "total", "gasto", "despesa", "finanças", "ajuda"])
        
        assert has_context, f"Resposta não parece contextual: {result['response']}"
        
        print(f"\n=== RESPOSTA COM HISTÓRICO ===")
        print(f"Resposta: {result['response']}")
