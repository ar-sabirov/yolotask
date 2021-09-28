import asyncio
import concurrent
from functools import partial
from typing import Optional

import aiohttp
from fastapi import FastAPI, Query, status, Response

from yolotask.config import settings
from yolotask.db.storages import RedisStorage
from yolotask.models import RequestModel, StatsResponseModel
from yolotask.utils.stats import process_stats

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.state.db = RedisStorage(settings.db_url)
    await app.state.db.connect()


@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


@app.post("/GetAd", status_code=status.HTTP_200_OK)
async def get_ad(body: RequestModel):
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.resource_url) as resp:
            res = await resp.text()
    await app.state.db.save_request(body)
    return Response(media_type='application/xml', content=res)


@app.post("/Impression", status_code=status.HTTP_200_OK)
async def impression(body: RequestModel):
    await app.state.db.save_impression(body)


# TODO add title and description to query
@app.get("/GetStats", status_code=status.HTTP_200_OK)
async def read_item(
    filter_type: Optional[str] = Query(default="user", alias="FilterType", regex=r"^(user|sdk)$"),
) -> StatsResponseModel:
    ad_requests, impressions = await app.state.db.get_stats(filter_type)
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool,
            partial(process_stats, ad_requests=ad_requests, impressions=impressions),
        )

    return result
