import logging
from typing import Optional
from app.domain.grading.dimensions import get_eval_focus, compute_weighted_score
from app.domain.grading.validator import OutputValidator, AssessmentResult
from app.domain.grading.prompt_manager import PromptManager
from app.infrastructure.llm.base import LLMProvider
from app.infrastructure.llm.circuit_breaker import CostCircuitBreaker
from app.infrastructure.cache.similarity import SimilarityCache


logger = logging.getLogger(__name__)


class GradingEngine:
    """评分引擎 — 核心领域逻辑"""

    def __init__(
        self,
        llm: LLMProvider,
        validator: OutputValidator,
        prompt_manager: PromptManager,
        circuit_breaker: CostCircuitBreaker,
        similarity_cache: SimilarityCache,
    ):
        self.llm = llm
        self.validator = validator
        self.prompts = prompt_manager
        self.breaker = circuit_breaker
        self.cache = similarity_cache

    async def assess(
        self,
        student_id: str,
        class_id: str,
        grade: int,
        topic: str,
        response: str
    ) -> dict:
        """评估学生发言 — 主入口"""

        # 1. 成本熔断检查
        budget = await self.breaker.check_and_consume(student_id, class_id)
        if not budget["allowed"]:
            logger.warning(f"Cost limit exceeded: student={student_id}, reason={budget['reason']}")
            return self._budget_exceeded_result(budget["reason"])

        # 2. 相似缓存检查
        cached = await self.cache.get_cached_result(grade, topic, response)
        if cached:
            logger.info(f"Cache hit: student={student_id}")
            cached["from_cache"] = True
            return cached

        # 3. 渲染Prompt并调用LLM
        prompt = self.prompts.render_assessment_prompt(grade, topic, response)
        eval_focus = get_eval_focus(grade)

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"【评估重点】{eval_focus}\n\n请严格按JSON格式返回评估结果。"}
        ]

        try:
            raw_output = await self.llm.chat(
                messages=messages,
                temperature=0,
                response_format={"type": "json_object"}
            )
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return self._error_result(str(e))

        # 4. 校验 + 修复
        result: AssessmentResult = await self.validator.validate_and_fix(raw_output)

        # 5. 组装返回
        output = {
            "scores": result.scores,
            "weighted_score": compute_weighted_score(result.scores, grade),
            "reasoning": result.reasoning,
            "highlights": result.highlights,
            "suggestions": result.suggestions,
            "overall_comment": result.overall_comment,
            "from_cache": False,
        }

        # 6. 写入缓存
        await self.cache.cache_result(grade, topic, response, output)

        return output

    def _budget_exceeded_result(self, reason: str) -> dict:
        return {
            "scores": {},
            "weighted_score": 0,
            "reasoning": f"评估次数已用完（{reason}），请联系老师手动评估",
            "highlights": "",
            "suggestions": "",
            "overall_comment": "已达评估上限",
            "error": True,
            "error_type": reason,
        }

    def _error_result(self, error_msg: str) -> dict:
        return {
            "scores": {"观点清晰度": 3, "逻辑连贯性": 3, "证据支撑": 3,
                       "多角度思考": 3, "回应与质疑": 3, "表达完整性": 3},
            "weighted_score": 3.0,
            "reasoning": f"[系统异常] {error_msg[:80]}",
            "highlights": "系统处理中遇到问题",
            "suggestions": "建议老师手动评估",
            "overall_comment": "系统评估异常，已标记待人工复核",
            "error": True,
            "error_type": "llm_error",
        }
