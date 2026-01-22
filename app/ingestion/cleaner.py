import re

def clean_text(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)          # Normalize whitespace
    text = re.sub(r"\n+", "\n", text)          # Collapse newlines
    text = re.sub(r"Page \d+", "", text)       # Remove page numbers
    text = re.sub(r"\x0c", "", text)           # Remove form feed chars

    return text.strip()
