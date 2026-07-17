from app.tasks import celery_app


@celery_app.task(bind=True, max_retries=3)
def assess_response_task(self, student_id: str, class_id: str, grade: int, topic: str, response: str):
    """评估任务"""
    try:
        # TODO: 注入依赖并调用GradingEngine
        return {"status": "success", "student_id": student_id}
    except Exception as exc:
        self.retry(exc=exc, countdown=5)
