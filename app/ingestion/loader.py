import os
import pdfplumber
import docx
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text as pdfminer_extract_text


def load_document(path: str) -> str:
    """
    Robust document loader with safe fallbacks.
    Never crashes. Never OCRs. Enterprise-safe.
    """

    ext = os.path.splitext(path)[1].lower()

    try:
        # --------------------
        # PDF handling
        # --------------------
        if ext == ".pdf":
            text = ""

            # First attempt: pdfplumber (fast, layout-aware)
            try:
                with pdfplumber.open(path) as pdf:
                    pages = [p.extract_text() or "" for p in pdf.pages]
                    text = "\n".join(pages).strip()
            except Exception:
                text = ""

            # Fallback: pdfminer (robust, encoding-safe)
            if not text:
                try:
                    text = pdfminer_extract_text(path) or ""
                except Exception:
                    text = ""

            return text.strip()

        # --------------------
        # DOCX handling
        # --------------------
        if ext == ".docx":
            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs).strip()

        # --------------------
        # HTML handling
        # --------------------
        if ext in [".html", ".htm"]:
            with open(path, encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f, "html.parser")
                return soup.get_text(separator=" ").strip()

        # --------------------
        # Unsupported formats
        # --------------------
        return ""

    except Exception:
        # Absolute safety net
        return ""
