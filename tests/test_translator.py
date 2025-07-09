from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure src package is on path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

import translator  # noqa: E402
import translate as translate_cli  # noqa: E402


def test_load_glossary(tmp_path: Path) -> None:
    csv_file = tmp_path / "glossary.csv"
    csv_file.write_text("en,hu\nhello,szia\nworld,vilag\n", encoding="utf-8")
    result = translator.load_glossary(csv_file)
    assert result == {"hello": "szia", "world": "vilag"}


def test_translate_text() -> None:
    glossary = {"hello": "szia", "world": "vilag"}
    translated = translator.translate_text("hello world", glossary)
    assert translated == "szia vilag"


def test_translate_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    csv_file = tmp_path / "g.csv"
    csv_file.write_text("en,hu\nhello,szia\n", encoding="utf-8")
    argv = [
        "translate.py",
        "--glossary",
        str(csv_file),
        "--text",
        "hello",
    ]
    sys.argv = argv
    translate_cli.main()
    out = capsys.readouterr().out.strip()
    assert out == "szia"
