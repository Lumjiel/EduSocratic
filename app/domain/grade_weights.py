"""年级差异化权重"""

from app.domain.constants import DIMENSIONS

# 每个年级段的权重（键顺序与 DIMENSIONS 一致）
GRADE_WEIGHTS: dict[str, dict[str, float]] = {
    "1_2": {
        "观点清晰度": 0.30,
        "逻辑连贯性": 0.00,  # 不评估
        "证据支撑": 0.25,
        "多角度思考": 0.00,  # 不评估
        "回应与质疑": 0.20,
        "表达完整性": 0.25,
    },
    "3_4": {
        "观点清晰度": 0.25,
        "逻辑连贯性": 0.15,
        "证据支撑": 0.20,
        "多角度思考": 0.15,
        "回应与质疑": 0.15,
        "表达完整性": 0.10,
    },
    "5_7": {
        "观点清晰度": 0.20,
        "逻辑连贯性": 0.20,
        "证据支撑": 0.20,
        "多角度思考": 0.20,
        "回应与质疑": 0.10,
        "表达完整性": 0.10,
    },
}


def get_grade_band(grade: int) -> str:
    """年级 → 年级段"""
    if grade in (1, 2):
        return "1_2"
    elif grade in (3, 4):
        return "3_4"
    else:  # 5, 6, 7
        return "5_7"


def get_weights(grade: int) -> dict[str, float]:
    """获取指定年级的权重"""
    band = get_grade_band(grade)
    return GRADE_WEIGHTS[band]


def get_active_dimensions(grade: int) -> list[str]:
    """获取该年级实际评估的维度（权重>0的）"""
    weights = get_weights(grade)
    return [dim for dim in DIMENSIONS if weights[dim] > 0]


def compute_weighted_score(scores: dict[str, int], grade: int) -> float:
    """计算加权总分"""
    weights = get_weights(grade)
    total = sum(scores[dim] * weights[dim] for dim in DIMENSIONS)
    return round(total, 2)
