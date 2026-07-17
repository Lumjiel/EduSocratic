import pytest
from app.domain.grading.dimensions import (
    get_weights_for_grade,
    get_eval_focus,
    compute_weighted_score,
    DIMENSION_NAMES,
)


class TestDimensions:
    def test_get_weights_grade_1(self):
        weights = get_weights_for_grade(1)
        assert "观点清晰度" in weights
        assert weights["观点清晰度"] == 0.40
        assert weights["表达完整性"] == 0.30

    def test_get_weights_grade_3(self):
        weights = get_weights_for_grade(3)
        assert weights["逻辑连贯性"] == 0.25
        assert weights["证据支撑"] == 0.25

    def test_get_weights_grade_5(self):
        weights = get_weights_for_grade(5)
        assert weights["多角度思考"] == 0.20
        assert weights["回应与质疑"] == 0.20

    def test_eval_focus_exists(self):
        focus = get_eval_focus(1)
        assert len(focus) > 0

    def test_compute_weighted_score(self):
        scores = {"观点清晰度": 4, "逻辑连贯性": 3, "证据支撑": 4,
                  "多角度思考": 2, "回应与质疑": 3, "表达完整性": 4}
        result = compute_weighted_score(scores, 3)
        assert 1 <= result <= 5

    def test_all_dimensions_present(self):
        assert len(DIMENSION_NAMES) == 6
        assert "观点清晰度" in DIMENSION_NAMES
        assert "逻辑连贯性" in DIMENSION_NAMES
