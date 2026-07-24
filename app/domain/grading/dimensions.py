from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class DimensionDefinition:
    name: str
    description: str

    def __str__(self) -> str:
        return self.name


@dataclass
class GradeWeightConfig:
    grade_range: str
    weights: Dict[str, float]
    eval_focus: str

    def validate(self) -> bool:
        total = sum(self.weights.values())
        return abs(total - 1.0) < 0.01


DIMENSIONS: Dict[str, DimensionDefinition] = {
    "观点清晰度": DimensionDefinition(
        name="观点清晰度",
        description="学生是否明确表达了自己的立场和观点"
    ),
    "逻辑连贯性": DimensionDefinition(
        name="逻辑连贯性",
        description="论证是否有因果关系、是否自洽"
    ),
    "证据支撑": DimensionDefinition(
        name="证据支撑",
        description="是否举出例子或引用事实支撑观点"
    ),
    "多角度思考": DimensionDefinition(
        name="多角度思考",
        description="是否考虑不同立场或反方观点"
    ),
    "回应与质疑": DimensionDefinition(
        name="回应与质疑",
        description="是否有效回应或质疑他人观点"
    ),
    "表达完整性": DimensionDefinition(
        name="表达完整性",
        description="语言是否完整、有条理"
    ),
}

DIMENSION_NAMES = list(DIMENSIONS.keys())

GRADE_WEIGHTS: Dict[int, GradeWeightConfig] = {
    1: GradeWeightConfig(
        grade_range="1-2年级",
        weights={
            "观点清晰度": 0.40,
            "表达完整性": 0.30,
            "证据支撑": 0.15,
            "回应与质疑": 0.15,
            "逻辑连贯性": 0.0,
        },
        eval_focus="能说出来就是进步 —— 重点评估'是否愿意表达'和'能否说出基本观点'"
    ),
    2: GradeWeightConfig(
        grade_range="1-2年级",
        weights={
            "观点清晰度": 0.40,
            "表达完整性": 0.30,
            "证据支撑": 0.15,
            "回应与质疑": 0.15,
            "逻辑连贯性": 0.0,
        },
        eval_focus="能说出来就是进步 —— 重点评估'是否愿意表达'和'能否说出基本观点'"
    ),
    3: GradeWeightConfig(
        grade_range="3-4年级",
        weights={
            "观点清晰度": 0.30,
            "逻辑连贯性": 0.25,
            "证据支撑": 0.25,
            "多角度思考": 0.10,
            "回应与质疑": 0.10,
            "表达完整性": 0.0,
        },
        eval_focus="能讲出道理就是成长 —— 重点评估论证的基本逻辑和证据意识"
    ),
    4: GradeWeightConfig(
        grade_range="3-4年级",
        weights={
            "观点清晰度": 0.30,
            "逻辑连贯性": 0.25,
            "证据支撑": 0.25,
            "多角度思考": 0.10,
            "回应与质疑": 0.10,
            "表达完整性": 0.0,
        },
        eval_focus="能讲出道理就是成长 —— 重点评估论证的基本逻辑和证据意识"
    ),
    5: GradeWeightConfig(
        grade_range="5-7年级",
        weights={
            "逻辑连贯性": 0.25,
            "多角度思考": 0.20,
            "证据支撑": 0.20,
            "回应与质疑": 0.20,
            "观点清晰度": 0.15,
            "表达完整性": 0.0,
        },
        eval_focus="能辩证思考就是深度 —— 重点评估批判性思维的高阶能力"
    ),
    6: GradeWeightConfig(
        grade_range="5-7年级",
        weights={
            "逻辑连贯性": 0.25,
            "多角度思考": 0.20,
            "证据支撑": 0.20,
            "回应与质疑": 0.20,
            "观点清晰度": 0.15,
            "表达完整性": 0.0,
        },
        eval_focus="能辩证思考就是深度 —— 重点评估批判性思维的高阶能力"
    ),
    7: GradeWeightConfig(
        grade_range="5-7年级",
        weights={
            "逻辑连贯性": 0.25,
            "多角度思考": 0.20,
            "证据支撑": 0.20,
            "回应与质疑": 0.20,
            "观点清晰度": 0.15,
            "表达完整性": 0.0,
        },
        eval_focus="能辩证思考就是深度 —— 重点评估批判性思维的高阶能力"
    ),
}


def get_weights_for_grade(grade: int) -> Dict[str, float]:
    config = GRADE_WEIGHTS.get(grade, GRADE_WEIGHTS[3])
    return {k: v for k, v in config.weights.items() if v > 0}


def get_eval_focus(grade: int) -> str:
    config = GRADE_WEIGHTS.get(grade, GRADE_WEIGHTS[3])
    return config.eval_focus


def compute_weighted_score(scores: Dict[str, int], grade: int) -> float:
    weights = get_weights_for_grade(grade)
    total = 0.0
    weight_sum = 0.0
    for dim, score in scores.items():
        if dim in weights:
            total += score * weights[dim]
            weight_sum += weights[dim]
    return round(total / weight_sum, 2) if weight_sum > 0 else 3.0
