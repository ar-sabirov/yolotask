from typing import Dict, Tuple

import aioredis
from yolotask.models import RequestModel


class RedisStorageClient:
    def __init__(self, url: str) -> None:
        self.redis: aioredis.Redis = None
        self.url = url

    def connect(self) -> None:
        pool = aioredis.ConnectionPool.from_url(self.url, max_connections=10)
        self.redis = aioredis.Redis(connection_pool=pool)

    async def close(self) -> None:
        await self.redis.close()

    async def save_request(self, request: RequestModel) -> None:
        await self.redis.hincrby("user_requests", f"{request.user_name}")
        await self.redis.hincrby("sdk_requests", f"{request.sdk_version}")

    async def save_impression(self, request: RequestModel) -> None:
        await self.redis.hincrby("user_impressions", f"{request.user_name}")
        await self.redis.hincrby("sdk_impressions", f"{request.sdk_version}")

    async def get_stats(self, agg: str) -> Tuple[Dict[str, int], Dict[str, int]]:
        requests = await self._hscanget(f"{agg}_requests")
        impressions = await self._hscanget(f"{agg}_impressions")

        return requests, impressions

    async def _hscanget(self, name: str) -> Dict[str, int]:
        data: Dict[str, int] = {}
        cur = b"0"  # set initial cursor to 0
        while cur:
            cur, keys = await self.redis.hscan(name, cur)
            if not keys:
                return data
            values = await self.redis.hmget(name, keys)
            values = map(int, values)
            data.update(dict(zip(keys, values)))

        return data
