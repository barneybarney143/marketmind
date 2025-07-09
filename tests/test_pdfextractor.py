from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw
from fpdf import FPDF

# ensure src path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

import pdfextractor  # noqa: E402
import extract_pdf as extract_cli  # noqa: E402


def create_text_pdf(path: Path, text: str) -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=text, ln=True)
    pdf.output(str(path))


def create_image_pdf(path: Path, text: str) -> None:
    img = Image.new("RGB", (200, 50), "white")
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill="black")
    img_path = path.with_suffix(".png")
    img.save(img_path)
    pdf = FPDF()
    pdf.add_page()
    pdf.image(str(img_path), x=10, y=10, w=100)
    pdf.output(str(path))
    img_path.unlink()


def test_extract_text_direct(tmp_path: Path) -> None:
    pdf_file = tmp_path / "direct.pdf"
    create_text_pdf(pdf_file, "Hello world")
    result = pdfextractor.extract_text_from_pdf(pdf_file)
    assert "Hello world" in result


def test_extract_text_ocr(tmp_path: Path) -> None:
    pdf_file = tmp_path / "ocr.pdf"
    create_image_pdf(pdf_file, "OCR test")
    result = pdfextractor.extract_text_from_pdf(pdf_file)
    assert "OCR" in result


def test_cli_output(tmp_path: Path) -> None:
    pdf_file = tmp_path / "cli.pdf"
    create_text_pdf(pdf_file, "CLI works")
    out_file = tmp_path / "out.txt"
    argv = [
        "extract_pdf.py",
        str(pdf_file),
        "--output",
        str(out_file),
    ]
    sys.argv = argv
    extract_cli.main()
    content = out_file.read_text(encoding="utf-8")
    assert "CLI works" in content
