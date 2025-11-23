import os
from celery import Celery

# TODO: get redis urls from enviroment variables, with defaults
broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

# celery config
celery_app = Celery("worker", broker=broker_url, backend=result_backend)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # timeout for task
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
    # memory and performance optimizations for my t3.small :(
    worker_max_tasks_per_child=10,  # restart worker after 10 tasks
    worker_prefetch_multiplier=1,  # fetch 1 task at a time for now due to small serger
    task_acks_late=True,  # acknowledge tasks after completion
    worker_pool_restarts=True,  # enable worker pool restarts
    # auto expire results after 1 hour to prevent memory leaks
    result_expires=3600,
)
