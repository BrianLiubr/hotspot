SOURCES = [
    {"name": "OpenAI Blog", "type": "rss", "url": "https://openai.com/news/rss.xml", "category_default": "ai", "weight": 1.0},
    {"name": "Hugging Face Blog", "type": "rss", "url": "https://huggingface.co/blog/feed.xml", "category_default": "ai", "weight": 1.0},
    {"name": "中国新闻网", "type": "page", "url": "https://www.chinanews.com.cn/", "category_default": "society", "weight": 1.0},
]


if __name__ == "__main__":
    for source in SOURCES:
        print(source)
