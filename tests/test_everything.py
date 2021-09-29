import aiohttp
import pytest


@pytest.mark.asyncio
async def test_everything():
    body = {
        "SDK Version": "1.2",
        "SessionId": "abc",
        "Platform": "ios",
        "User name": "everyday regular normal mf",
        "Country code": "ca",
    }
    async with aiohttp.ClientSession(headers={"content-type": "application/json"}) as session:
        resp1 = await session.post("http://127.0.0.1:8000/GetAd", json=body)
        resp2 = await session.post("http://127.0.0.1:8000/GetAd", json=body)

        async with resp1, resp2:
            assert resp1.status == 200
            assert resp2.status == 200

        response = await session.post("http://127.0.0.1:8000/Impression", json=body)
        async with response:
            assert response.status == 200

        async with session.get("http://127.0.0.1:8000/GetStats?FilterType=user") as response:
            data = await response.json()

            user = body["User name"]
            assert data["ad_requests"][user] == 2
            assert data["impressions"][user] == 1
            assert data["fill_rate"][user] == 0.5
