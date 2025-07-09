from __future__ import annotations

import argparse
from pathlib import Path

import sys
from pathlib import Path as _Path

# Allow running without installing the package
repo_root = _Path(__file__).resolve().parent
sys.path.insert(0, str(repo_root / "src"))

from pdfextractor import extract_text_from_pdf  # noqa: E402


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
