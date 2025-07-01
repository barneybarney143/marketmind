from __future__ import annotations

import sys
from pathlib import Path

import pytest

import track_prompt
import analyze_cognitive_load


def test_track_prompt_logging(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    log_file = tmp_path / "log.md"
    long_prompt = (
        "This is a very long prompt that should be shortened when it is logged "
        "because it exceeds the limit. Extra text to ensure we go past the "
        "threshold."
    )
    argv = [
        "track_prompt.py",
        "--prompt",
        long_prompt,
        "--session-id",
        "test",
        "--project",
        "proj",
        "--file",
        "file.txt",
        "--log",
        str(log_file),
    ]
    monkeypatch.setattr(sys, "argv", argv)
    track_prompt.main()
    assert log_file.exists()
    content = log_file.read_text()
    assert "complexity_score" in content
    expected = track_prompt.shorten_prompt(long_prompt)
    assert expected in content


def test_analyze_cognitive_load(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    log_file = tmp_path / "log.md"
    # create two entries to trigger no overload
    log_file.write_text(
        "## 2030-01-01T00:00\n"
        "complexity_score: 0.1\n"
        "quality: high\n"
        "tokens_estimate: 5\n"
    )
    monkeypatch.chdir(tmp_path)
    result = analyze_cognitive_load.analyze(
        analyze_cognitive_load.parse_logs(log_file),
        analyze_cognitive_load.load_config(),
    )
    assert result is False

