from typing import Optional


class ReportGenerator:
    """报告生成器"""

    def __init__(self, feishu_client):
        self.feishu = feishu_client

    async def generate_weekly_report(
        self,
        student_id: int,
        classroom_id: int,
        period_start: str,
        period_end: str
    ) -> dict:
        """生成学生周学习报告"""
        # TODO: 从数据库获取学生评估记录，生成报告
        return {
            "student_id": student_id,
            "period": f"{period_start} ~ {period_end}",
            "doc_url": "",
            "status": "not_implemented"
        }
