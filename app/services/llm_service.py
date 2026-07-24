"""LLM 调用封装：调用 + 校验 + 修复重试 + 兜底"""

import json
import logging
from openai import AsyncOpenAI
from pydantic import ValidationError

from app.config import settings
from app.domain.schemas import LLMAssessmentOutput, AssessmentResult
from app.domain.grade_weights import compute_weighted_score
from app.prompts import render_assessment_prompt
from app.prompts.repair import REPAIR_PROMPT

logger = logging.getLogger(__name__)

# 模块级 client 保持可 patch（测试直接替换 app.services.llm_service.client）。
# 未配置 OPENAI_API_KEY 时置 None：真实调用会落入兜底分支（needs_review=True），系统不崩。
try:
    client = AsyncOpenAI(api_key=settings.openai_api_key)
except Exception as e:
    logger.warning(f"OpenAI client 初始化失败（未配置 API key？），将以兜底模式运行: {e}")
    client = None


async def call_llm_assessment(
    text: str,
    grade: int,
    topic: str,
    student_id: str,
    class_id: str,
    source_type: str = "text",
    teacher_context: str | None = None,
    retry_count: int = 0,
) -> AssessmentResult:
    """
    完整的 LLM 评估调用。
    包含：调用 → 校验 → 修复重试 → 兜底。
    """
    messages = render_assessment_prompt(
        grade=grade, topic=topic, text=text, teacher_context=teacher_context
    )

    raw_output = ""
    last_error = ""

    for attempt in range(settings.llm_max_retries + 1):
        try:
            # 调用 LLM
            if attempt == 0:
                # 首次调用
                response = await client.chat.completions.create(
                    model=settings.openai_model,
                    messages=messages,
                    temperature=0,
                    max_tokens=2000,
                    timeout=settings.llm_timeout,
                )
            else:
                # 修复重试
                repair_msg = REPAIR_PROMPT.format(
                    error_message=last_error,
                    raw_output=raw_output[:500],
                )
                response = await client.chat.completions.create(
                    model=settings.openai_model,
                    messages=messages + [
                        {"role": "assistant", "content": raw_output},
                        {"role": "user", "content": repair_msg},
                    ],
                    temperature=0,
                    max_tokens=2000,
                    timeout=settings.llm_timeout,
                )

            raw_output = response.choices[0].message.content or ""

            # 三段式校验
            parsed = _validate_output(raw_output)

            # 构建结果
            scores = {
                "观点清晰度": parsed.观点清晰度,
                "逻辑连贯性": parsed.逻辑连贯性,
                "证据支撑": parsed.证据支撑,
                "多角度思考": parsed.多角度思考,
                "回应与质疑": parsed.回应与质疑,
                "表达完整性": parsed.表达完整性,
            }

            weighted = compute_weighted_score(scores, grade)

            return AssessmentResult(
                scores=scores,
                weighted_score=weighted,
                reasoning=parsed.reasoning,
                highlights=parsed.highlights,
                suggestions=parsed.suggestions,
                overall_comment=parsed.overall_comment,
                needs_review=False,
                grade=grade,
                topic=topic,
                student_id=student_id,
                class_id=class_id,
                source_type=source_type,
                retry_count=retry_count,
                teacher_context=teacher_context,
            )

        except ValidationError as e:
            last_error = str(e)
            logger.warning(f"校验失败 (attempt {attempt}): {last_error}")
            continue

        except json.JSONDecodeError as e:
            last_error = f"JSON 解析失败: {e}"
            logger.warning(f"JSON 解析失败 (attempt {attempt}): {last_error}")
            continue

        except Exception as e:
            last_error = str(e)
            logger.error(f"LLM 调用异常 (attempt {attempt}): {last_error}")
            break  # 非校验错误，直接兜底

    # 所有重试失败 → 兜底
    return _build_fallback(grade, topic, student_id, class_id, source_type, retry_count)


def _validate_output(raw: str) -> LLMAssessmentOutput:
    """三段式校验"""
    # 第一段：提取 JSON
    cleaned = raw.strip()
    # 去除可能的 markdown 代码块标记
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines)

    data = json.loads(cleaned)  # 可能抛 JSONDecodeError

    # 第二段 + 第三段：Pydantic 校验（结构 + 值域）
    return LLMAssessmentOutput(**data)  # 可能抛 ValidationError


def _build_fallback(
    grade: int, topic: str, student_id: str, class_id: str,
    source_type: str, retry_count: int,
) -> AssessmentResult:
    """构建兜底结果"""
    scores = {dim: 3 for dim in [
        "观点清晰度", "逻辑连贯性", "证据支撑",
        "多角度思考", "回应与质疑", "表达完整性",
    ]}
    weighted = compute_weighted_score(scores, grade)

    return AssessmentResult(
        scores=scores,
        weighted_score=weighted,
        reasoning="评估暂时不可用，已标记待人工复核。",
        highlights="待人工复核后补充。",
        suggestions="待人工复核后补充。",
        overall_comment="系统暂时无法完成评估，请稍后重试或等待人工处理。",
        needs_review=True,
        grade=grade,
        topic=topic,
        student_id=student_id,
        class_id=class_id,
        source_type=source_type,
        retry_count=retry_count,
    )
