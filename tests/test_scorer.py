from datetime import datetime, timezone

from app.services.ranking.scorer import score_item


def test_score_item():
    score = score_item("OpenAI Blog", datetime.now(timezone.utc), related_count=2, keyword_hits=3, category="ai")
    assert score > 0


def test_related_count_boost():
    low = score_item("Google News AI", datetime.now(timezone.utc), related_count=1, keyword_hits=1, category="ai")
    high = score_item("Google News AI", datetime.now(timezone.utc), related_count=4, keyword_hits=1, category="ai")
    assert high > low
