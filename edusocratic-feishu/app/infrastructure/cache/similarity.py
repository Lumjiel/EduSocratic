import hashlib
import redis.asyncio as redis
from typing import Optional
from app.config import settings


class SimilarityCache:
    """基于哈希的相似回答缓存"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.ttl = settings.CACHE_TTL

    def _compute_key(self, grade: int, topic: str, response: str) -> str:
        """计算缓存key"""
        raw = f"{grade}:{topic}:{response[:100]}"
        fingerprint = hashlib.md5(raw.encode("utf-8")).hexdigest()[:16]
        return f"assess:cache:{fingerprint}"

    async def get_cached_result(self, grade: int, topic: str, response: str) -> Optional[dict]:
        """查询是否有相似评估结果"""
        key = self._compute_key(grade, topic, response)
        cached = await self.redis.get(key)
        if cached:
            import json
            return json.loads(cached)
        return None

    async def cache_result(self, grade: int, topic: str, response: str, result: dict):
        """缓存评估结果"""
        key = self._compute_key(grade, topic, response)
        import json
        await self.redis.setex(key, self.ttl, json.dumps(result, ensure_ascii=False))
