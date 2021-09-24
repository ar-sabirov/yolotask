from fastapi import FastAPI, Query, Request

from models import RequestModel
from db.storages import RedisStorage

import aiohttp

app = FastAPI()


@app.on_event("startup")
async def startup():
    db = RedisStorage(host="localhost", port=6379)
    await db.connect()
    app.state.db = db


@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


@app.post("/GetAd")
async def get_ad(body: RequestModel, request: Request):
    res = "Hey"
    # TODO uncomment this
    # async with aiohttp.ClientSession() as session:
    #     async with session.get('https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast') as resp:
    #         res = await resp.text()
    await app.state.db.save_request(body.user_name)
    return res


@app.post("/Impression")
def impression(request: RequestModel):
    pass


# TODO add title and description to query
@app.get("/GetStats")
def read_item(
    filter_type: str = Query(default="user", alias="FilterType", regex=r"^(user|sdk)$"),
):
    return "WOW"
