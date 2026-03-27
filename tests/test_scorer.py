from datetime import datetime, timezone

from app.services.ranking.scorer import score_item


def test_score_item():
    score = score_item("OpenAI Blog", datetime.now(timezone.utc), related_count=2, keyword_hits=3)
    assert score > 0
