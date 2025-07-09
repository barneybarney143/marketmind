from __future__ import annotations

import argparse
from pathlib import Path

import sys
from pathlib import Path as _Path

# Allow running without installing the package
repo_root = _Path(__file__).resolve().parent
sys.path.insert(0, str(repo_root / "src"))

from translator import load_glossary, translate_text  # noqa: E402


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
