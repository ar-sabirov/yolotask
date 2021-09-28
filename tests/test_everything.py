import json

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from yolotask.server import app


class MockResponse:
    def __init__(self, text, status):
        self._text = text
        self.status = status

    async def text(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


@pytest.mark.asyncio
async def test_root(mocker):
    msg = json.dumps({'message': 'Hi from mock'})
    resp = MockResponse(msg, 200)
    mocker.patch("aiohttp.ClientSession.get", return_value=resp)

    data = {
        "SDK Version": "1.2",
        "SessionId": "abc",
        "Platform": "ios",
        "User name": "another regular normal mf",
        "Country code": "ca",
    }
    async with AsyncClient(app=app, base_url="http://test") as client, LifespanManager(app):
        response = await client.post("/GetAd", json=data)
    assert response.status_code == 200
