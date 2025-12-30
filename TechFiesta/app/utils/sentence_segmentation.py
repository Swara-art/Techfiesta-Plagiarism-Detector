import re

def segment_sentences(text: str) -> list[str]:
    if not text:
        return []

    text = text.replace("\n", " ").strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [s.strip() for s in sentences if s.strip()]
