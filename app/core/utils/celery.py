from celery import Celery

def create_celery_app():
    celery = Celery(
        "worker",
        broker="redis://redis:6379/0",  # Change this to your Redis configuration
        backend="redis://redis:6379/0"  # Same Redis instance for result backend
    )

    # Load configuration if any (optional)
    celery.conf.update(task_serializer='json', accept_content=['json'])

    return celery
