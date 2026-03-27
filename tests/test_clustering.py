from app.services.dedup.deduper import is_similar_title


def test_cluster_similarity_threshold():
    assert is_similar_title('openai发布新模型', 'openai发布新模型引发讨论', threshold=70) is True
