from typing import Any

import feedparser

from app.services.fetchers.base import BaseFetcher


class RSSFetcher(BaseFetcher):
    async def fetch(self, source: dict[str, Any]) -> list[dict[str, Any]]:
        feed = feedparser.parse(source["url"])
        items = []
        for entry in feed.entries[: source.get("max_items", 20)]:
            items.append(
                {
                    "title": getattr(entry, "title", ""),
                    "summary": getattr(entry, "summary", ""),
                    "url": getattr(entry, "link", ""),
                    "published_at": getattr(entry, "published", None),
                    "source": source["name"],
                }
            )
        return items
