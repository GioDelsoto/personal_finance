from typing import Protocol, Any
from celery import Task


class InterfaceQueueProducer(Protocol):
    """
    Interface for queue producers using Protocol (duck typing).
    
    This defines the contract that any queue producer must follow.
    No inheritance needed - just implement the methods.
    """
    
    def enqueue(self, task: Task, *args: Any, **kwargs: Any) -> Any:
        """
        Enqueue a task for standard execution.
        
        Args:
            task: Celery task to enqueue
            *args: Positional arguments for the task
            **kwargs: Keyword arguments for the task
            
        Returns:
            Task result object with task_id
        """
        ...
    
    def enqueue_with_options(
        self,
        task: Task,
        *args: Any,
        countdown: int | None = None,
        eta: Any | None = None,
        queue: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Enqueue a task with advanced options.
        
        Args:
            task: Celery task to enqueue
            *args: Positional arguments for the task
            countdown: Seconds to wait before execution
            eta: Specific datetime for execution
            queue: Specific queue name
            **kwargs: Keyword arguments for the task
            
        Returns:
            Task result object with task_id
        """
        ...
