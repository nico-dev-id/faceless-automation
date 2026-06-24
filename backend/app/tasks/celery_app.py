from celery import Celery

celery_app = Celery(
    "faceless_automation",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.tasks.video_tasks"]
)

celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
)