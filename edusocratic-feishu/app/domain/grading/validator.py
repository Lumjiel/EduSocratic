import json
import re
from pydantic import BaseModel, Field, validator
from typing import Dict, Optional
from .dimensions import DIMENSION_NAMES


class AssessmentResult(BaseModel):
    """评估结果数据模型 — 严格校验LLM输出"""
    scores: Dict[str, int] = Field(..., description="六维评分")
    reasoning: str = Field(..., min_length=10, max_length=500)
    highlights: str = Field(..., min_length=5, max_length=200)
    suggestions: str = Field(..., min_length=5, max_length=200)
    overall_comment: str = Field(..., min_length=20, max_length=100)

    @validator("scores")
    def validate_scores(cls, v):
        for dim in DIMENSION_NAMES:
            if dim not in v:
                raise ValueError(f"缺少维度: {dim}")
            if not isinstance(v[dim], (int, float)):
                raise ValueError(f"{dim} 分数必须是数字")
            v[dim] = int(v[dim])
            if not 1 <= v[dim] <= 5:
                raise ValueError(f"{dim} 分数 {v[dim]} 超出1-5范围")
        return v

    @validator("reasoning")
    def validate_reasoning(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("理由过短，至少10个字符")
        return v


class OutputValidator:
    """LLM输出校验 + 格式修复"""

    def __init__(self, llm_client, max_retries: int = 3):
        self.llm = llm_client
        self.max_retries = max_retries

    async def validate_and_fix(self, raw_output: str) -> AssessmentResult:
        """校验原始输出，失败则进入修复循环"""
        try:
            data = self._extract_json(raw_output)
            return AssessmentResult(**data)
        except (json.JSONDecodeError, Exception):
            pass

        for attempt in range(self.max_retries - 1):
            try:
                fixed = await self.llm.chat(
                    messages=[
                        {"role": "system", "content": FORMAT_REPAIR_PROMPT},
                        {"role": "user", "content": f"请修复以下JSON:\n{raw_output}"}
                    ],
                    temperature=0,
                    response_format={"type": "json_object"}
                )
                data = json.loads(fixed)
                return AssessmentResult(**data)
            except (json.JSONDecodeError, Exception):
                continue

        return self._fallback_result(raw_output)

    def _fallback_result(self, original: str) -> AssessmentResult:
        """兜底：中性分 + 保留原始输出供人工审查"""
        return AssessmentResult(
            scores={dim: 3 for dim in DIMENSION_NAMES},
            reasoning=f"[AI评估异常，需人工复核] 原始输出: {original[:100]}",
            highlights="AI评估异常",
            suggestions="建议老师手动评估本条",
            overall_comment="系统评估异常，已标记待人工复核"
        )

    def _extract_json(self, text: str) -> dict:
        """从LLM返回中提取JSON（处理Markdown包裹等情况）"""
        text = text.strip()
        if "```" in text:
            parts = text.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                try:
                    return json.loads(part)
                except json.JSONDecodeError:
                    continue
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r'\{[^{}]*"scores"[^{}]*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise


FORMAT_REPAIR_PROMPT = """你是一个JSON格式修复助手。你的任务是将用户提供的文本修复为合法的JSON。

要求：
1. 必须包含 "scores" 对象，其中有6个维度：观点清晰度、逻辑连贯性、证据支撑、多角度思考、回应与质疑、表达完整性
2. 每个维度的分数必须是1-5之间的整数
3. 必须包含 "reasoning"（至少10字符）、"highlights"（至少5字符）、"suggestions"（至少5字符）、"overall_comment"（至少20字符）
4. 只输出纯JSON，不要任何解释文字"""
