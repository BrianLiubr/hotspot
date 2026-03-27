import hashlib
import re
from html import unescape
from typing import Any


TAG_RE = re.compile(r"<[^>]+>")


def normalize_title(title: str) -> str:
    title = title.strip().lower()
    title = re.sub(r"\s+", "", title)
    title = re.sub(r"[^\w\u4e00-\u9fff]", "", title)
    return title


def clean_html_text(text: str) -> str:
    text = unescape(text or "")
    text = TAG_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_content_hash(title: str, url: str) -> str:
    raw = f"{normalize_title(title)}::{url}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    title = clean_html_text(item.get("title", "").strip())
    url = item.get("url", "").strip()
    summary = clean_html_text(item.get("summary", "").strip())
    return {
        **item,
        "title": title,
        "summary": summary,
        "url": url,
        "normalized_title": normalize_title(title),
        "content_hash": build_content_hash(title, url) if title and url else None,
        "language": "zh",
    }
