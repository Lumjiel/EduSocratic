import time
import logging
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志 + 链路追踪"""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        request.state.request_id = request_id

        logger.info(f"[{request_id}] {request.method} {request.url.path} started")

        try:
            response = await call_next(request)
            duration = round((time.time() - start_time) * 1000, 2)
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Duration-ms"] = str(duration)
            logger.info(f"[{request_id}] {request.method} {request.url.path} completed in {duration}ms")
            return response
        except Exception as e:
            duration = round((time.time() - start_time) * 1000, 2)
            logger.error(f"[{request_id}] {request.method} {request.url.path} failed in {duration}ms: {e}")
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """简单限频中间件"""

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def dispatch(self, request: Request, call_next) -> Response:
        # TODO: 使用Redis实现分布式限频
        return await call_next(request)
