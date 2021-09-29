import asyncio
import concurrent
from functools import partial
from typing import Optional

import aiohttp
from fastapi import FastAPI, Query, status, Response

from yolotask.config import settings
from yolotask.db.redis_storage import RedisStorageClient
from yolotask.models import RequestModel, StatsResponseModel
from yolotask.utils.stats import process_stats

app = FastAPI()
aiohttp_session: aiohttp.ClientSession = aiohttp.ClientSession()
process_pool = concurrent.futures.ProcessPoolExecutor(max_workers=settings.max_workers)


@app.on_event("startup")
def startup() -> None:
    app.state.db = RedisStorageClient(settings.db_url)
    app.state.db.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await app.state.db.close()
    await aiohttp_session.close()
    process_pool.shutdown()


@app.post("/GetAd", status_code=status.HTTP_200_OK)
async def get_ad(body: RequestModel) -> Response:
    async with aiohttp_session.get(settings.resource_url) as resp:
        res = await resp.text()
    await app.state.db.save_request(body)
    return Response(media_type="application/xml", content=res)


@app.post("/Impression", status_code=status.HTTP_200_OK)
async def impression(body: RequestModel):
    await app.state.db.save_impression(body)


# TODO add title and description to query
@app.get("/GetStats", status_code=status.HTTP_200_OK, response_model=StatsResponseModel)
async def read_item(
    filter_type: Optional[str] = Query(default="user", alias="FilterType", regex=r"^(user|sdk)$"),
) -> StatsResponseModel:
    ad_requests, impressions = await app.state.db.get_stats(filter_type)

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        process_pool,
        partial(process_stats, ad_requests=ad_requests, impressions=impressions),
    )

    return result
