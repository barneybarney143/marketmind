"""CLI tool to log developer prompts and metadata."""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import textwrap

import yaml

# simple heuristics for complexity
CONJUNCTIONS = {"and", "or", "but", "so", "because", "though", "although", "however"}
LOGIC_OPERATORS = {"&&", "||", "!", "==", "!=", ">", "<", ">=", "<="}

DEFAULT_LOG_PATH = Path("logs/prompt_log.md")
MAX_PROMPT_LENGTH = 80


def shorten_prompt(text: str, max_len: int = MAX_PROMPT_LENGTH) -> str:
    """Return the text truncated to at most ``max_len`` characters."""
    if len(text) <= max_len:
        return text
    return textwrap.shorten(text, width=max_len, placeholder="...")


def estimate_tokens(text: str) -> int:
    """Rough token estimate based on character count."""
    return max(1, len(text) // 4)


def compute_readability(text: str) -> float:
    """Basic Flesch reading ease score."""
    sentences = max(text.count("."), 1)
    words = text.split()
    syllables = sum(count_syllables(word) for word in words)
    num_words = len(words) or 1
    words_per_sentence = num_words / sentences
    syllables_per_word = syllables / num_words
    return 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word


def count_syllables(word: str) -> int:
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev_char_was_vowel = False
    for char in word:
        if char in vowels:
            if not prev_char_was_vowel:
                count += 1
            prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False
    if word.endswith("e") and count > 1:
        count -= 1
    return count or 1


def compute_complexity(text: str) -> float:
    tokens = text.split()
    token_count = len(tokens) or 1
    conj = sum(1 for t in tokens if t.lower() in CONJUNCTIONS)
    logic = sum(1 for t in tokens if t in LOGIC_OPERATORS)
    return (conj + logic) / token_count


def quality_from_readability(score: float) -> str:
    if score >= 60:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def append_log(log_path: Path, entry_time: datetime, data: dict[str, object]) -> None:
    log_path.parent.mkdir(exist_ok=True)
    if log_path.exists():
        contents = log_path.read_text()
    else:
        contents = ""
    with log_path.open("a") as f:
        if contents and not contents.endswith("\n"):
            f.write("\n")
        f.write(f"## {entry_time.isoformat(timespec='minutes')}\n")
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True, help="Prompt text")
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--project", default="unknown")
    parser.add_argument("--file", default="unknown")
    parser.add_argument("--log", default=str(DEFAULT_LOG_PATH), help="Log file path")
    args = parser.parse_args()

    raw_prompt = args.prompt
    short_prompt = shorten_prompt(raw_prompt)

    complexity = compute_complexity(raw_prompt)
    readability = compute_readability(raw_prompt)
    tokens = estimate_tokens(raw_prompt)
    quality = quality_from_readability(readability)

    data = {
        "complexity_score": round(complexity, 2),
        "quality": quality,
        "tokens_estimate": tokens,
        "session_id": args.session_id,
        "project": args.project,
        "file": args.file,
        "prompt": short_prompt,
    }

    log_path = Path(args.log)
    append_log(log_path, datetime.utcnow(), data)


if __name__ == "__main__":
    main()
