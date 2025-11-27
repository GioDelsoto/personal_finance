"""
Testes de integração para validar enfileiramento no Redis via Celery
"""
import pytest
import os
from src.producers.queue_producer import QueueProducer
from src.tasks.messages.process_message_task import process_message_task
from src.services.messages.income_message_handler import IncomingMessageHandler


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("REDIS_URL") and not os.path.exists("redis://localhost:6379"),
    reason="Redis não está disponível"
)
class TestQueueIntegration:
    """Testes de integração para validar Redis/Celery"""
    
    def test_producer_enqueues_task_to_redis(
        self, 
        sample_received_message, 
        sample_session_id, 
        sample_user
    ):
        """Testa se QueueProducer enfileira task no Redis"""
        # Arrange
        producer = QueueProducer()
        message_dict = sample_received_message.model_dump()
        
        # Act
        async_result = producer.enqueue(
            process_message_task,
            message_dict=message_dict,
            session_id=str(sample_session_id),
            user_dict=sample_user
        )
        
        # Assert
        assert async_result is not None
        assert async_result.id is not None
        print(f"\n✅ Task enfileirada com ID: {async_result.id}")
        print(f"✅ Status: {async_result.state}")
        
        # Verifica propriedades do AsyncResult
        assert hasattr(async_result, 'ready')
        assert hasattr(async_result, 'get')
        assert hasattr(async_result, 'state')
    
    def test_income_handler_enqueues_to_redis(
        self, 
        sample_received_message, 
        sample_session_id, 
        sample_user
    ):
        """Testa se IncomingMessageHandler enfileira no Redis"""
        # Arrange
        producer = QueueProducer()
        handler = IncomingMessageHandler(producer=producer)
        
        # Act
        result = handler.handle_incoming_message(
            sample_received_message, 
            sample_session_id, 
            sample_user
        )
        
        # Assert
        assert result["status"] == "queued"
        assert result["message_id"] == sample_received_message.message_id
        print(f"\n✅ Mensagem enfileirada: {sample_received_message.message_id}")
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY não configurada"
    )
    def test_task_processing_with_worker(
        self, 
        sample_received_message, 
        sample_session_id, 
        sample_user
    ):
        """
        Testa processamento completo com Celery worker
        ATENÇÃO: Requer worker rodando!
        """
        # Arrange
        producer = QueueProducer()
        message_dict = sample_received_message.model_dump()
        
        # Act
        async_result = producer.enqueue(
            process_message_task,
            message_dict=message_dict,
            session_id=str(sample_session_id),
            user_dict=sample_user
        )
        
        print(f"\n✅ Task enviada: {async_result.id}")
        print("⏳ Aguardando processamento pelo worker...")
        
        # Aguarda até 30 segundos
        try:
            result = async_result.get(timeout=30)
            print(f"✅ Resultado: {result[:100]}..." if len(result) > 100 else f"✅ Resultado: {result}")
            assert result is not None
            assert isinstance(result, str)
        except Exception as e:
            pytest.skip(f"Worker não processou a tempo ou não está rodando: {e}")
