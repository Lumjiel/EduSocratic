import logging
from datetime import datetime, timedelta
from typing import Optional


logger = logging.getLogger(__name__)


class FeedbackCollector:
    """收集教师对AI评分的修正，用于后续优化"""

    def __init__(self, db_session):
        self.db = db_session

    async def record_disagreement(
        self,
        assessment_id: int,
        teacher_id: int,
        original_scores: dict,
        corrected_scores: dict,
        feedback_reason: Optional[str] = None
    ) -> dict:
        """记录一次教师修正"""

        diff = {}
        for dim in original_scores:
            diff[dim] = corrected_scores.get(dim, 3) - original_scores.get(dim, 3)

        max_diff_dim = max(diff, key=lambda k: abs(diff[k]))

        feedback = {
            "assessment_id": assessment_id,
            "teacher_id": teacher_id,
            "original_scores": original_scores,
            "corrected_scores": corrected_scores,
            "differences": diff,
            "max_disagreement_dimension": max_diff_dim,
            "max_disagreement_value": diff[max_diff_dim],
            "reason": feedback_reason,
            "created_at": datetime.utcnow()
        }

        # TODO: 写入数据库
        logger.info(f"Feedback recorded: assessment={assessment_id}, max_diff={max_diff_dim}")

        await self._check_prompt_drift(max_diff_dim)
        return feedback

    async def _check_prompt_drift(self, dimension: str):
        """检测Prompt是否需要调整"""
        # TODO: 查询数据库统计近7天该维度的修正次数
        pass


class FeedbackAnalyzer:
    """分析教师反馈数据，输出优化建议"""

    def __init__(self, db_session):
        self.db = db_session

    async def get_dimension_drift_report(self, days: int = 7) -> dict:
        """生成各维度偏差报告"""
        # TODO: 从数据库聚合分析
        return {
            "period_days": days,
            "dimensions": {},
            "recommendation": "数据不足，需要更多教师反馈"
        }
