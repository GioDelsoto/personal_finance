from typing import Any, Dict, Optional
from celery import Task

class QueueProducer:
    @staticmethod
    def enqueue(task: Task, *args: Any, **kwargs: Any):
        """
        Envia a task para execução padrão.
        """
        return task.apply_async(aargs=args, kwargs=kwargs)

    @staticmethod
    def enqueue_with_options(
        task: Task,
        *args: Any,
        countdown: Optional[int] = None,
        eta: Optional[Any] = None,
        queue: Optional[str] = None,
        **kwargs: Any,
    ):
        """
        Envia task com opções avançadas
        """
        options: Dict[str, Any] = {}

        if countdown is not None:
            options["countdown"] = countdown
        if eta is not None:
            options["eta"] = eta
        if queue is not None:
            options["queue"] = queue

        return task.apply_async(args=args, kwargs=kwargs, **options)
