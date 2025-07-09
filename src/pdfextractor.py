from __future__ import annotations

from pathlib import Path

from pdfminer.high_level import extract_text as pdfminer_extract_text
from pdf2image import convert_from_path
import pytesseract  # type: ignore[import-untyped]


def extract_text_from_pdf(path: Path, *, ocr_lang: str = "eng") -> str:
    """Return text content from *path*.

    First attempts direct extraction using :mod:`pdfminer`. If that yields no
    text, fall back to OCR using :mod:`pytesseract`.
    """
    text = pdfminer_extract_text(str(path))
    if text.strip():
        return text
    images = convert_from_path(str(path))
    ocr_text = "\n".join(
        pytesseract.image_to_string(image, lang=ocr_lang) for image in images
    )
    return ocr_text
