from typing import Any

import httpx
from bs4 import BeautifulSoup

from app.services.fetchers.base import BaseFetcher


class PageFetcher(BaseFetcher):
    async def fetch(self, source: dict[str, Any]) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(source["url"])
            response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.text.strip() if soup.title else source["name"]
        return [{"title": title, "summary": "", "url": source["url"], "source": source["name"]}]
