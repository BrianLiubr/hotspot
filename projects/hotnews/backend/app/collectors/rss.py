from datetime import datetime

import feedparser

from app.collectors.base import BaseCollector
from app.services import CollectedItem


class ExampleRssCollector(BaseCollector):
    name = "example_rss"
    source_type = "rss"
    base_url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

    def collect(self) -> list[CollectedItem]:
        feed = feedparser.parse(self.base_url)
        items: list[CollectedItem] = []
        for index, entry in enumerate(feed.entries[:30]):
            published_at = None
            if getattr(entry, "published", None):
                published_at = entry.published
            items.append(
                CollectedItem(
                    source_name=self.name,
                    title=getattr(entry, "title", "(untitled)"),
                    summary=getattr(entry, "summary", None),
                    url=getattr(entry, "link", f"urn:example-rss:{index}:{datetime.utcnow().timestamp()}"),
                    published_at=published_at,
                    rank_score=float(max(1, 100 - index)),
                    category="news",
                )
            )
        return items
