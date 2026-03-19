from datetime import datetime, timedelta

from app.collectors.base import BaseCollector
from app.config import TIMEZONE
from app.services import CollectedItem


class SampleStaticCollector(BaseCollector):
    name = "sample_static"
    source_type = "static"
    base_url = "https://example.com/hotnews-demo"

    def collect(self) -> list[CollectedItem]:
        now = datetime.now(TIMEZONE)
        yesterday = now - timedelta(days=1)
        two_days_ago = now - timedelta(days=2)
        return [
            CollectedItem(
                source_name=self.name,
                title="示例热点：开源数据源聚合上线",
                summary="这是一个本地静态示例源，用于验证 API 和数据库流程。",
                url="https://example.com/news/opensource-hotnews",
                published_at=two_days_ago,
                rank_score=95.0,
                category="tech",
            ),
            CollectedItem(
                source_name=self.name,
                title="示例热点：昨日新闻摘要",
                summary="用于演示“默认截至前一天”的查询逻辑。",
                url="https://example.com/news/yesterday-brief",
                published_at=yesterday,
                rank_score=90.0,
                category="general",
            ),
        ]
