from abc import ABCMeta

import aioredis
from yolotask.models import RequestModel


class AbstractStorage(metaclass=ABCMeta):
    async def save_request(user_id):
        pass

    async def save_impression():
        pass


class RedisStorage(AbstractStorage):
    def __init__(self, url: str) -> None:
        self.redis_client: aioredis.Redis = None
        self.url = url

    async def connect(self):
        self.redis_client: aioredis.Redis = await aioredis.from_url(
            self.url,
            encoding="utf-8",
            decode_responses=True,
        )

    async def close(self):
        self.redis_client.close()
        await self.redis_client.wait_closed()

    async def save_request(self, request: RequestModel):
        await self.redis_client.hincrby("user_requests", f"{request.user_name}")
        await self.redis_client.hincrby("sdk_requests", f"{request.sdk_version}")

    async def save_impression(self, request: RequestModel):
        await self.redis_client.hincrby("user_impressions", f"{request.user_name}")
        await self.redis_client.hincrby("sdk_impressions", f"{request.sdk_version}")

    async def get_stats(self, agg: str):

        requests = await self._hscanget(f"{agg}_requests")
        impressions = await self._hscanget(f"{agg}_impressions")

        return requests, impressions

    async def _hscanget(self, name: str):
        data = {}
        cur = b"0"  # set initial cursor to 0
        while cur:
            cur, keys = await self.redis_client.hscan(name, cur)
            if not keys:
                return data
            values = await self.redis_client.hmget(name, keys)
            values = map(int, values)
            data.update(dict(zip(keys, values)))

        return data
