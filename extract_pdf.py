from __future__ import annotations

import argparse
from pathlib import Path

from pdfextractor import extract_text_from_pdf


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF using pdfminer or OCR"
    )
    parser.add_argument("pdf", type=Path, help="Path to PDF file")
    parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Output text file"
    )
    parser.add_argument(
        "--lang",
        default="eng",
        help="Tesseract language code for OCR",
    )
    args = parser.parse_args()

    text = extract_text_from_pdf(args.pdf, ocr_lang=args.lang)
    args.output.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
