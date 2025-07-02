"""Analyze prompt logs and warn about possible overload."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import sys

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "tracker_config.yaml"
DEFAULT_LOG_PATH = PROJECT_ROOT / "logs" / "prompt_log.md"


@dataclass
class PromptEntry:
    timestamp: datetime
    complexity: float
    quality: str


def parse_logs(log_path: Path) -> list[PromptEntry]:
    entries: list[PromptEntry] = []
    if not log_path.exists():
        return entries
    text = log_path.read_text().splitlines()
    current_time: datetime | None = None
    current_data: dict[str, str | float] = {}
    for line in text:
        if line.startswith("## "):
            if current_time is not None:
                entries.append(
                    PromptEntry(
                        current_time,
                        float(current_data.get("complexity_score", 0)),
                        str(current_data.get("quality", "")),
                    )
                )
            current_time = datetime.fromisoformat(line[3:])
            current_data = {}
        elif line.startswith("```"):
            continue
        elif ":" in line:
            key, value = line.split(":", 1)
            current_data[key.strip()] = value.strip()
    if current_time is not None:
        entries.append(
            PromptEntry(
                current_time,
                float(current_data.get("complexity_score", 0)),
                str(current_data.get("quality", "")),
            )
        )
    return entries


def load_config() -> dict[str, float | str]:
    if CONFIG_PATH.exists():
        data = yaml.safe_load(CONFIG_PATH.read_text())
        if isinstance(data, dict):
            return {str(k): v for k, v in data.items()}
    return {}


def analyze(entries: list[PromptEntry], config: dict[str, float | str]) -> bool:
    now = datetime.utcnow()
    one_hour = now - timedelta(hours=1)
    six_hours = now - timedelta(hours=6)
    day_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    recent_1h = [e for e in entries if e.timestamp > one_hour]
    recent_6h = [e for e in entries if e.timestamp > six_hours]
    today = [e for e in entries if e.timestamp > day_start]

    max_prompts_hour = int(config.get("max_prompts_hour", 20))
    max_complexity_avg = float(config.get("max_complexity_avg_hour", 0.6))
    max_active_hours = float(config.get("max_active_hours_day", 8))
    complex_threshold = float(config.get("complex_threshold", 0.7))

    overload = False

    if len(recent_1h) > max_prompts_hour:
        print("High number of prompts in last hour")
        overload = True

    if recent_1h:
        avg_complexity = sum(e.complexity for e in recent_1h) / len(recent_1h)
        if avg_complexity > max_complexity_avg:
            print("Average complexity high in last hour")
            overload = True

    low_quality_streak = 0
    for e in reversed(entries):
        if e.quality.lower() in {"low", ""}:
            low_quality_streak += 1
        else:
            break
    if low_quality_streak >= 3:
        print("Multiple low quality prompts detected")
        overload = True

    if today:
        start = min(e.timestamp for e in today)
        end = max(e.timestamp for e in today)
        active_hours = (end - start).seconds / 3600
        if active_hours > max_active_hours:
            print("Long active time today")
            overload = True

    complex_count = sum(1 for e in recent_6h if e.complexity > complex_threshold)
    if complex_count > max_prompts_hour:
        print("Many complex prompts recently")
        overload = True

    return overload


def main() -> None:
    config = load_config()
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LOG_PATH
    entries = parse_logs(log_path)
    overload = analyze(entries, config)
    if overload:
        Path(".you-need-a-break").touch()
        print("Warning: cognitive load may be high")
        sys.exit(1)
    print("Cognitive load normal")


if __name__ == "__main__":
    main()
