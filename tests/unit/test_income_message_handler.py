"""
Testes unitários para IncomingMessageHandler
"""
from unittest.mock import MagicMock
from src.services.messages.income_message_handler import IncomingMessageHandler


class TestIncomingMessageHandler:
    """Testes para IncomingMessageHandler"""
    
    def test_handle_incoming_message_enqueues_task(
        self, 
        sample_received_message, 
        sample_session_id, 
        sample_user
    ):
        """Testa se handle_incoming_message enfileira a task corretamente"""
        # Arrange
        mock_producer = MagicMock()
        handler = IncomingMessageHandler(producer=mock_producer)
        
        # Act
        result = handler.handle_incoming_message(
            sample_received_message, 
            sample_session_id, 
            sample_user
        )
        
        # Assert
        mock_producer.enqueue.assert_called_once()
        call_args = mock_producer.enqueue.call_args
        
        # Verifica que a task foi passada
        assert call_args[0][0].__name__ == "process_message_task"
        
        # Verifica os kwargs
        kwargs = call_args[1]
        assert kwargs["message_dict"]["message_id"] == sample_received_message.message_id
        assert kwargs["message_dict"]["phone"] == sample_received_message.phone
        assert kwargs["message_dict"]["text"] == sample_received_message.text
        assert kwargs["session_id"] == str(sample_session_id)
        assert kwargs["user_dict"] == sample_user
        
        # Verifica retorno
        assert result["status"] == "queued"
        assert result["message_id"] == sample_received_message.message_id
