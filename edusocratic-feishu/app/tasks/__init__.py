from celery import Celery
from app.config import settings

celery_app = Celery(
    "edusocratic",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.assessment", "app.tasks.report"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    worker_prefetch_multiplier=1,
)


@celery_app.task(bind=True, max_retries=3)
def process_assessment(self, student_id: str, class_id: str, grade: int, topic: str, response: str):
    """异步评估任务"""
    try:
        # TODO: 调用GradingEngine进行评估
        return {"status": "success", "student_id": student_id}
    except Exception as exc:
        self.retry(exc=exc, countdown=5)


@celery_app.task(bind=True, max_retries=3)
def generate_report(self, student_id: int, classroom_id: int, period_start: str, period_end: str):
    """异步报告生成任务"""
    try:
        # TODO: 生成学习报告
        return {"status": "success", "student_id": student_id}
    except Exception as exc:
        self.retry(exc=exc, countdown=10)
