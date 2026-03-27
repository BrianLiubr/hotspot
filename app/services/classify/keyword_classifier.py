AI_KEYWORDS = ["ai", "大模型", "agent", "openai", "anthropic", "gemini", "claude", "芯片", "英伟达"]
FINANCE_KEYWORDS = ["a股", "港股", "美股", "财报", "降息", "通胀", "央行", "黄金", "原油", "汇率"]
SOCIETY_KEYWORDS = ["通报", "警方", "法院", "教育", "医疗", "事故", "地震", "消防", "民生", "政策"]


CATEGORY_KEYWORDS = {
    "ai": AI_KEYWORDS,
    "finance": FINANCE_KEYWORDS,
    "society": SOCIETY_KEYWORDS,
}


def classify_text(title: str, summary: str = "") -> tuple[str, dict[str, int]]:
    text = f"{title} {summary}".lower()
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for keyword in keywords if keyword.lower() in text)
    best_category = max(scores, key=scores.get) if scores else "society"
    if scores.get(best_category, 0) == 0:
        best_category = "society"
    return best_category, scores
