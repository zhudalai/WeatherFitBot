import json
import time
from typing import Optional

try:
    import redis.asyncio as redis

    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

from app.config import settings


class MemoryCache:
    """内存缓存（Redis 不可用时的降级方案）"""

    def __init__(self):
        self._data: dict[str, tuple[str, float]] = {}

    async def get(self, key: str) -> Optional[str]:
        if key in self._data:
            value, expire_at = self._data[key]
            if time.time() < expire_at:
                return value
            del self._data[key]
        return None

    async def set(self, key: str, value: str, ttl: int = 900):
        self._data[key] = (value, time.time() + ttl)

    async def get_json(self, key: str) -> Optional[dict]:
        data = await self.get(key)
        if data:
            return json.loads(data)
        return None

    async def set_json(self, key: str, value: dict, ttl: int = 900):
        await self.set(key, json.dumps(value, default=str), ttl)


class RedisCache:
    """Redis 缓存封装，不可用时自动降级为内存缓存"""

    def __init__(self):
        self._redis: Optional[object] = None
        self._memory = MemoryCache()
        self._use_redis = False

    async def connect(self):
        """建立连接"""
        if not HAS_REDIS:
            return
        try:
            self._redis = redis.from_url(settings.redis_url, decode_responses=True)
            await self._redis.ping()
            self._use_redis = True
        except Exception:
            self._use_redis = False

    async def disconnect(self):
        """关闭连接"""
        if self._redis and self._use_redis:
            await self._redis.close()

    async def get(self, key: str) -> Optional[str]:
        if self._use_redis and self._redis:
            try:
                return await self._redis.get(key)
            except Exception:
                pass
        return await self._memory.get(key)

    async def set(self, key: str, value: str, ttl: int = 900):
        if self._use_redis and self._redis:
            try:
                await self._redis.setex(key, ttl, value)
                return
            except Exception:
                pass
        await self._memory.set(key, value, ttl)

    async def get_json(self, key: str) -> Optional[dict]:
        data = await self.get(key)
        if data:
            return json.loads(data)
        return None

    async def set_json(self, key: str, value: dict, ttl: int = 900):
        await self.set(key, json.dumps(value, default=str), ttl)


cache = RedisCache()
