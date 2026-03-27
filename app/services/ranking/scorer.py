from datetime import datetime, timezone


SOURCE_WEIGHT = {
    "OpenAI Blog": 24,
    "Anthropic Blog": 22,
    "Google AI Blog": 20,
    "Hugging Face Blog": 20,
    "Google News AI": 14,
    "Google News Finance": 14,
    "Google News Society": 14,
    "新华社": 22,
    "中国新闻网": 18,
}

CATEGORY_WEIGHT = {
    "ai": 6,
    "finance": 5,
    "society": 4,
}


def freshness_score(published_at: datetime | None) -> int:
    if not published_at:
        return 5
    now = datetime.now(timezone.utc)
    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=timezone.utc)
    delta_hours = (now - published_at).total_seconds() / 3600
    if delta_hours <= 1:
        return 36
    if delta_hours <= 3:
        return 28
    if delta_hours <= 6:
        return 20
    if delta_hours <= 12:
        return 12
    if delta_hours <= 24:
        return 7
    return 3


def score_item(source_name: str, published_at: datetime | None, related_count: int = 1, keyword_hits: int = 0, category: str | None = None) -> int:
    return (
        SOURCE_WEIGHT.get(source_name, 10)
        + CATEGORY_WEIGHT.get(category or "", 0)
        + freshness_score(published_at)
        + min((related_count - 1) * 6, 24)
        + min(keyword_hits * 2, 14)
    )
