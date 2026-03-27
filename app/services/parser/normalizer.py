import hashlib
import re
from typing import Any


def normalize_title(title: str) -> str:
    title = title.strip().lower()
    title = re.sub(r"\s+", "", title)
    title = re.sub(r"[^\w\u4e00-\u9fff]", "", title)
    return title


def build_content_hash(title: str, url: str) -> str:
    raw = f"{normalize_title(title)}::{url}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    title = item.get("title", "").strip()
    url = item.get("url", "").strip()
    return {
        **item,
        "title": title,
        "summary": item.get("summary", "").strip(),
        "url": url,
        "normalized_title": normalize_title(title),
        "content_hash": build_content_hash(title, url) if title and url else None,
        "language": "zh",
    }
