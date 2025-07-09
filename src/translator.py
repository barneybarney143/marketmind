from __future__ import annotations

import csv
from pathlib import Path


def load_glossary(path: Path) -> dict[str, str]:
    """Return a dictionary mapping English terms to Hungarian."""
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or set(reader.fieldnames) != {"en", "hu"}:
            raise ValueError("Glossary must have 'en' and 'hu' columns")
        glossary: dict[str, str] = {}
        for row in reader:
            en = row.get("en") or ""
            hu = row.get("hu") or ""
            if en:
                glossary[en.strip().lower()] = hu.strip()
    return glossary


def translate_text(
    text: str, glossary: dict[str, str], *, reverse: bool = False
) -> str:
    """Translate a space-separated text using *glossary*.

    If *reverse* is True, translate Hungarian to English."""
    dictionary = glossary if not reverse else {v: k for k, v in glossary.items()}
    words = text.split()
    translated = [dictionary.get(w.lower(), w) for w in words]
    return " ".join(translated)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Simple glossary-based translator"
    )
    parser.add_argument(
        "glossary", type=Path, help="CSV file with 'en' and 'hu' columns"
    )
    parser.add_argument("text", help="Text to translate")
    parser.add_argument("--reverse", action="store_true", help="Translate hu->en")
    args = parser.parse_args()

    glossary = load_glossary(args.glossary)
    result = translate_text(args.text, glossary, reverse=args.reverse)
    print(result)
