import redis.asyncio as redis
from datetime import datetime
from app.config import settings


class CostCircuitBreaker:
    """API成本熔断器"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.daily_limit = settings.DAILY_LIMIT_PER_STUDENT
        self.monthly_budget = settings.MONTHLY_BUDGET_PER_CLASS
        self.per_request_cost = settings.PER_REQUEST_COST

    async def check_and_consume(self, student_id: str, class_id: str) -> dict:
        """检查是否允许本次评估，允许则扣减预算"""
        now = datetime.now()
        daily_key = f"cost:daily:{student_id}:{now.strftime('%Y%m%d')}"
        monthly_key = f"cost:monthly:{class_id}:{now.strftime('%Y%m')}"

        daily_count = int(await self.redis.get(daily_key) or 0)
        if daily_count >= self.daily_limit:
            return {"allowed": False, "reason": "daily_limit_exceeded"}

        monthly_cost = float(await self.redis.get(monthly_key) or 0)
        if monthly_cost + self.per_request_cost > self.monthly_budget:
            return {"allowed": False, "reason": "monthly_budget_exceeded"}

        pipe = self.redis.pipeline()
        pipe.incr(daily_key)
        pipe.expire(daily_key, 86400)
        pipe.incrbyfloat(monthly_key, self.per_request_cost)
        pipe.expire(monthly_key, 2592000)
        await pipe.execute()

        return {
            "allowed": True,
            "daily_remaining": self.daily_limit - daily_count - 1,
            "monthly_remaining": round(self.monthly_budget - monthly_cost - self.per_request_cost, 2)
        }

    async def get_usage(self, student_id: str, class_id: str) -> dict:
        """获取当前用量"""
        now = datetime.now()
        daily_key = f"cost:daily:{student_id}:{now.strftime('%Y%m%d')}"
        monthly_key = f"cost:monthly:{class_id}:{now.strftime('%Y%m')}"

        daily_count = int(await self.redis.get(daily_key) or 0)
        monthly_cost = float(await self.redis.get(monthly_key) or 0)

        return {
            "daily_used": daily_count,
            "daily_limit": self.daily_limit,
            "daily_remaining": max(0, self.daily_limit - daily_count),
            "monthly_used": round(monthly_cost, 2),
            "monthly_budget": self.monthly_budget,
            "monthly_remaining": round(max(0, self.monthly_budget - monthly_cost), 2),
        }
