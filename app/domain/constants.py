"""评估维度与常量定义"""

# 六个评估维度（固定顺序）
DIMENSIONS: tuple[str, ...] = (
    "观点清晰度",
    "逻辑连贯性",
    "证据支撑",
    "多角度思考",
    "回应与质疑",
    "表达完整性",
)

# 分数范围
SCORE_MIN = 1
SCORE_MAX = 5

# 年级范围
GRADE_MIN = 1
GRADE_MAX = 7

# 文本长度限制
TEXT_MIN_LENGTH = 10
TEXT_MAX_LENGTH = 2000

# 打回次数上限
MAX_RETRY_COUNT = 2


# 评估状态
class AssessmentStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    MODIFIED = "modified"
    RETRYING = "retrying"
    DISPUTED = "disputed"
    RESOLVED = "resolved"


# 来源类型
class SourceType:
    HANDWRITING = "handwriting"
    VOICE = "voice"
    TEXT = "text"
