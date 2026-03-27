from app.services.classify.keyword_classifier import classify_text


def test_classify_ai_text():
    category, scores = classify_text("OpenAI 发布新 AI Agent")
    assert category == "ai"
    assert scores["ai"] > 0
