import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "faceless_automation",
    broker=REDIS_URL + "?ssl_cert_reqs=none",
    backend=REDIS_URL + "?ssl_cert_reqs=none",
    include=["app.tasks.video_tasks"]
)

celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
)