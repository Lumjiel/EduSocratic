"""Level 1 验收测试：领域模型"""


def test_grade_weights_sum_to_one():
    """每个年级段的权重之和必须为 1.0"""
    from app.domain.grade_weights import GRADE_WEIGHTS
    for band, weights in GRADE_WEIGHTS.items():
        total = sum(weights.values())
        assert abs(total - 1.0) < 0.001, f"{band} 权重之和为 {total}"


def test_grade_1_2_excludes_logic_and_perspective():
    """1-2年级不评估逻辑连贯性和多角度思考"""
    from app.domain.grade_weights import get_weights
    w = get_weights(1)
    assert w["逻辑连贯性"] == 0.0
    assert w["多角度思考"] == 0.0


def test_compute_weighted_score():
    """加权总分计算正确"""
    from app.domain.grade_weights import compute_weighted_score
    scores = {"观点清晰度": 4, "逻辑连贯性": 3, "证据支撑": 4,
              "多角度思考": 3, "回应与质疑": 3, "表达完整性": 4}
    # 3-4年级权重
    result = compute_weighted_score(scores, grade=3)
    expected = 4 * 0.25 + 3 * 0.15 + 4 * 0.20 + 3 * 0.15 + 3 * 0.15 + 4 * 0.10
    assert abs(result - round(expected, 2)) < 0.01


def test_llm_output_validation_rejects_out_of_range():
    """分数越界应报错"""
    import pytest
    from app.domain.schemas import LLMAssessmentOutput
    with pytest.raises(Exception):
        LLMAssessmentOutput(
            观点清晰度=6,  # 越界
            逻辑连贯性=3, 证据支撑=3, 多角度思考=3,
            回应与质疑=3, 表达完整性=3,
            reasoning="test", highlights="test",
            suggestions="test", overall_comment="test"
        )


def test_llm_output_validation_rejects_float():
    """分数为小数应报错"""
    import pytest
    from app.domain.schemas import LLMAssessmentOutput
    with pytest.raises(Exception):
        LLMAssessmentOutput(
            观点清晰度=3.5,  # 小数
            逻辑连贯性=3, 证据支撑=3, 多角度思考=3,
            回应与质疑=3, 表达完整性=3,
            reasoning="test", highlights="test",
            suggestions="test", overall_comment="test"
        )


def test_parsed_command_defaults():
    """解析指令默认值"""
    from app.domain.schemas import ParsedCommand
    cmd = ParsedCommand(action="assess", raw_message="test")
    assert cmd.student_name is None
    assert cmd.grade is None
