"""Level 2 验收测试：LLM 调用封装"""

import json
import pytest
from unittest.mock import AsyncMock, patch


def _mock_response(content: str) -> AsyncMock:
    """构造 openai ChatCompletion mock 响应"""
    resp = AsyncMock()
    resp.choices = [AsyncMock()]
    resp.choices[0].message.content = content
    return resp


@pytest.mark.asyncio
async def test_call_llm_assessment_success():
    """正常调用返回完整结果"""
    mock_response = _mock_response(json.dumps({
        "观点清晰度": 4, "逻辑连贯性": 3, "证据支撑": 4,
        "多角度思考": 3, "回应与质疑": 3, "表达完整性": 4,
        "reasoning": "观点明确，有因果论证",
        "highlights": "能用因为所以来论证",
        "suggestions": "可以展开反方观点",
        "overall_comment": "达到三年级应有水平"
    }))

    with patch("app.services.llm_service.client") as mock_client:
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        from app.services.llm_service import call_llm_assessment
        result = await call_llm_assessment(
            text="我觉得应该给动物穿衣服，因为动物会冷。",
            grade=3, topic="动物穿衣服",
            student_id="s1", class_id="c1",
        )
        assert result.weighted_score > 0
        assert result.needs_review is False
        assert result.scores["观点清晰度"] == 4


@pytest.mark.asyncio
async def test_call_llm_assessment_fallback_on_timeout():
    """LLM 超时 → 兜底"""
    with patch("app.services.llm_service.client") as mock_client:
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("timeout"))
        from app.services.llm_service import call_llm_assessment
        result = await call_llm_assessment(
            text="test", grade=3, topic="test",
            student_id="s1", class_id="c1",
        )
        assert result.needs_review is True
        assert all(v == 3 for v in result.scores.values())


@pytest.mark.asyncio
async def test_call_llm_assessment_repair_retry():
    """第一次返回垃圾 → 触发修复重试 → 第二次成功"""
    garbage = _mock_response("这不是 JSON，是一段胡话")
    fixed = _mock_response(json.dumps({
        "观点清晰度": 3, "逻辑连贯性": 3, "证据支撑": 3,
        "多角度思考": 3, "回应与质疑": 3, "表达完整性": 3,
        "reasoning": "t", "highlights": "t",
        "suggestions": "t", "overall_comment": "t"
    }))

    with patch("app.services.llm_service.client") as mock_client:
        mock_client.chat.completions.create = AsyncMock(side_effect=[garbage, fixed])
        from app.services.llm_service import call_llm_assessment
        result = await call_llm_assessment(
            text="test", grade=3, topic="test",
            student_id="s1", class_id="c1",
        )
        assert result.needs_review is False
        assert mock_client.chat.completions.create.call_count == 2


def test_validate_output_rejects_markdown_wrapped():
    """能处理 markdown 代码块包裹的 JSON"""
    from app.services.llm_service import _validate_output
    raw = '```json\n{"观点清晰度":4,"逻辑连贯性":3,"证据支撑":4,"多角度思考":3,"回应与质疑":3,"表达完整性":4,"reasoning":"t","highlights":"t","suggestions":"t","overall_comment":"t"}\n```'
    result = _validate_output(raw)
    assert result.观点清晰度 == 4
