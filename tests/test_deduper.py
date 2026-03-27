from app.services.dedup.deduper import is_similar_title


def test_similar_title():
    assert is_similar_title("OpenAI 发布新模型", "OpenAI 发布新模型！") is True
