import logging
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel


logger = logging.getLogger(__name__)
router = APIRouter()


class AssessRequest(BaseModel):
    student_id: str
    class_id: str
    grade: int
    topic: str
    response: str


class AssessResponse(BaseModel):
    scores: dict
    weighted_score: float
    reasoning: str
    highlights: str
    suggestions: str
    overall_comment: str


@router.post("/assess", response_model=AssessResponse)
async def assess(request: Request, body: AssessRequest):
    """评估接口"""
    engine = request.app.state.engine
    result = await engine.assess(
        student_id=body.student_id,
        class_id=body.class_id,
        grade=body.grade,
        topic=body.topic,
        response=body.response,
    )
    if result.get("error"):
        raise HTTPException(status_code=429, detail=result.get("reasoning", "评估失败"))
    return AssessResponse(**result)


@router.get("/usage/{student_id}")
async def get_usage(request: Request, student_id: str, class_id: str = "default"):
    """查询用量"""
    breaker = request.app.state.breaker
    return await breaker.get_usage(student_id, class_id)
