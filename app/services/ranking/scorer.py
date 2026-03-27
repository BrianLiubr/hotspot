from datetime import datetime, timezone


SOURCE_WEIGHT = {
    "OpenAI Blog": 20,
    "Anthropic Blog": 18,
    "Google AI Blog": 18,
    "新华社": 20,
    "中国新闻网": 16,
}


def freshness_score(published_at: datetime | None) -> int:
    if not published_at:
        return 5
    now = datetime.now(timezone.utc)
    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=timezone.utc)
    delta_hours = (now - published_at).total_seconds() / 3600
    if delta_hours <= 2:
        return 30
    if delta_hours <= 6:
        return 20
    if delta_hours <= 24:
        return 10
    return 3


def score_item(source_name: str, published_at: datetime | None, related_count: int = 1, keyword_hits: int = 0) -> int:
    return SOURCE_WEIGHT.get(source_name, 10) + freshness_score(published_at) + min(related_count * 3, 15) + min(keyword_hits * 2, 10)
