from fastapi import APIRouter
from app.api.v1.webhooks import router as webhook_router
from app.api.v1.assessment import router as assessment_router
from app.api.v1.reports import router as reports_router

router = APIRouter()
router.include_router(webhook_router, prefix="/webhooks", tags=["webhooks"])
router.include_router(assessment_router, prefix="/v1", tags=["assessment"])
router.include_router(reports_router, prefix="/v1", tags=["reports"])
