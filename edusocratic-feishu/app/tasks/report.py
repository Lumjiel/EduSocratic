from app.tasks import celery_app


@celery_app.task(bind=True, max_retries=3)
def generate_weekly_report_task(self, student_id: int, classroom_id: int, period_start: str, period_end: str):
    """报告生成任务"""
    try:
        # TODO: 生成学习报告
        return {"status": "success", "student_id": student_id}
    except Exception as exc:
        self.retry(exc=exc, countdown=10)
