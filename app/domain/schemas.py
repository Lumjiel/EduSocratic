"""Pydantic 数据模型"""

from pydantic import BaseModel, Field, field_validator
from app.domain.constants import SCORE_MIN, SCORE_MAX, GRADE_MIN, GRADE_MAX


# ─── 评估输入 ───


class AssessmentInput(BaseModel):
    """评估请求输入"""
    text: str = Field(..., min_length=1, description="学生发言/作文文字")
    grade: int = Field(..., ge=GRADE_MIN, le=GRADE_MAX)
    topic: str = Field(..., min_length=1, max_length=100)
    student_id: str = Field(..., min_length=1)
    class_id: str = Field(..., min_length=1)
    source_type: str = Field(default="text")  # handwriting / voice / text
    teacher_context: str | None = None  # 打回时老师补充的上下文
    retry_count: int = Field(default=0, ge=0, le=2)


# ─── LLM 原始输出 ───


class LLMAssessmentOutput(BaseModel):
    """LLM 返回的原始评估结果（用于 Pydantic 校验）"""
    观点清晰度: int = Field(..., ge=SCORE_MIN, le=SCORE_MAX)
    逻辑连贯性: int = Field(..., ge=SCORE_MIN, le=SCORE_MAX)
    证据支撑: int = Field(..., ge=SCORE_MIN, le=SCORE_MAX)
    多角度思考: int = Field(..., ge=SCORE_MIN, le=SCORE_MAX)
    回应与质疑: int = Field(..., ge=SCORE_MIN, le=SCORE_MAX)
    表达完整性: int = Field(..., ge=SCORE_MIN, le=SCORE_MAX)
    reasoning: str = Field(..., min_length=1)
    highlights: str = Field(..., min_length=1)
    suggestions: str = Field(..., min_length=1)
    overall_comment: str = Field(..., min_length=1)

    @field_validator("观点清晰度", "逻辑连贯性", "证据支撑", "多角度思考", "回应与质疑", "表达完整性")
    @classmethod
    def score_must_be_int(cls, v):
        if not isinstance(v, int):
            raise ValueError(f"分数必须是整数，收到 {type(v)}")
        return v


# ─── 评估结果（完整） ───


class AssessmentResult(BaseModel):
    """完整评估结果（含加权分）"""
    scores: dict[str, int]  # 六维分数
    weighted_score: float = Field(..., ge=1.0, le=5.0)
    reasoning: str
    highlights: str
    suggestions: str
    overall_comment: str
    needs_review: bool = False
    grade: int
    topic: str
    student_id: str
    class_id: str
    source_type: str = "text"
    retry_count: int = 0
    teacher_context: str | None = None


# ─── 兜底结果 ───


class FallbackResult(BaseModel):
    """兜底结果（LLM 失败时）"""
    scores: dict[str, int]  # 全 3 分
    weighted_score: float
    reasoning: str = "评估暂时不可用，已标记待人工复核。"
    highlights: str = "待人工复核后补充。"
    suggestions: str = "待人工复核后补充。"
    overall_comment: str = "系统暂时无法完成评估，请稍后重试或等待人工处理。"
    needs_review: bool = True


# ─── 教师反馈 ───


class TeacherFeedback(BaseModel):
    """教师反馈"""
    assessment_id: int
    teacher_id: str
    action: str  # confirm / modify / disagree / retry
    modified_scores: dict[str, int] | None = None
    teacher_context: str | None = None
    comment: str | None = None


# ─── 飞书消息解析 ───


class ParsedCommand(BaseModel):
    """解析后的老师指令"""
    action: str  # assess / query / help / weekly_report / cancel
    student_name: str | None = None
    grade: int | None = None
    topic: str | None = None
    text: str | None = None  # 学生发言文字
    raw_message: str = ""
