from rapidfuzz import fuzz


def is_similar_title(title_a: str, title_b: str, threshold: int = 88) -> bool:
    if not title_a or not title_b:
        return False
    return fuzz.ratio(title_a, title_b) >= threshold
