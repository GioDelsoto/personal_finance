"""
Testes unitários para QueueProducer
"""
from unittest.mock import MagicMock
from src.producers.queue_producer import QueueProducer


class TestQueueProducer:
    """Testes para QueueProducer"""
    
    def test_enqueue_calls_apply_async(self):
        """Testa se enqueue chama apply_async corretamente"""
        # Arrange
        mock_task = MagicMock()
        mock_result = MagicMock()
        mock_result.id = "task-123"
        mock_task.apply_async.return_value = mock_result
        
        # Act
        result = QueueProducer.enqueue(
            mock_task,
            message_dict={"text": "test"},
            session_id="session-1"
        )
        
        # Assert
        mock_task.apply_async.assert_called_once()
        call_kwargs = mock_task.apply_async.call_args[1]
        assert "kwargs" in call_kwargs
        assert call_kwargs["kwargs"]["message_dict"] == {"text": "test"}
        assert call_kwargs["kwargs"]["session_id"] == "session-1"
        assert result.id == "task-123"
    
    def test_enqueue_with_options_countdown(self):
        """Testa enqueue_with_options com countdown"""
        # Arrange
        mock_task = MagicMock()
        mock_result = MagicMock()
        mock_result.id = "task-456"
        mock_task.apply_async.return_value = mock_result
        
        # Act
        result = QueueProducer.enqueue_with_options(
            mock_task,
            countdown=30,
            data="test_data"
        )
        
        # Assert
        mock_task.apply_async.assert_called_once()
        call_kwargs = mock_task.apply_async.call_args[1]
        assert call_kwargs["countdown"] == 30
        assert call_kwargs["kwargs"]["data"] == "test_data"
        assert result.id == "task-456"
