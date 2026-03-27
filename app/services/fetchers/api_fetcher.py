from typing import Any

import httpx

from app.services.fetchers.base import BaseFetcher


class APIFetcher(BaseFetcher):
    async def fetch(self, source: dict[str, Any]) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(source["url"])
            response.raise_for_status()
            payload = response.json()
        return payload if isinstance(payload, list) else payload.get("items", [])
