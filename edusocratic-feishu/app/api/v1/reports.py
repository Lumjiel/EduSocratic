import logging
from fastapi import APIRouter, Request
from pydantic import BaseModel


logger = logging.getLogger(__name__)
router = APIRouter()


class ReportRequest(BaseModel):
    student_id: int
    classroom_id: int
    period_start: str
    period_end: str


@router.post("/reports/generate")
async def generate_report(request: Request, body: ReportRequest):
    """生成学习报告"""
    # TODO: 调用报告生成服务
    return {"status": "not_implemented"}


@router.get("/reports/{student_id}")
async def get_reports(request: Request, student_id: int):
    """获取学生报告列表"""
    return {"reports": []}
