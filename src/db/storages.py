from abc import ABCMeta
import aioredis


class AbstractStorage(metaclass=ABCMeta):
    async def save_request(user_id):
        pass

    async def save_impression():
        pass


class RedisStorage(AbstractStorage):
    def __init__(self, host: str, port: int) -> None:
        self.redis_client: aioredis.Redis = None
        self.host = host
        self.port = port

    async def connect(self):
        self.redis_client: aioredis.Redis = await aioredis.from_url(
            "redis://default:123@localhost:6379/0",
            encoding="utf-8",
            decode_responses=True,
        )

    async def close(self):
        self.redis_client.close()
        await self.redis_client.wait_closed()

    async def save_request(self, user_name: str):
        await self.redis_client.incr(f"{user_name}_reqcnt")

    async def save_impression(self, user_name: str):
        await self.redis_client.incr(f"{user_name}_impcnt")
