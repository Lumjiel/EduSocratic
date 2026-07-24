import logging
import traceback
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class GlobalErrorHandler(BaseHTTPMiddleware):
    """全局异常处理中间件"""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unhandled exception: {e}\n{traceback.format_exc()}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "internal_server_error",
                    "message": "服务器内部错误，请稍后重试",
                    "request_id": getattr(request.state, "request_id", "unknown")
                }
            )
