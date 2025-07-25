from __future__ import annotations

import argparse
from pathlib import Path

from translator import load_glossary, translate_text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Translate text using a CSV glossary"
    )
    parser.add_argument(
        "--glossary",
        required=True,
        type=Path,
        help="CSV file with 'en' and 'hu' columns",
    )
    parser.add_argument("--text", required=True, help="Text to translate")
    parser.add_argument("--reverse", action="store_true", help="Translate hu->en")
    args = parser.parse_args()

    glossary = load_glossary(args.glossary)
    result = translate_text(args.text, glossary, reverse=args.reverse)
    print(result)


if __name__ == "__main__":
    main()
