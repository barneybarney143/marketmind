from __future__ import annotations

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

from scripts.backtest import generate_param_grid  # noqa: E402


def test_generate_param_grid() -> None:
    params = {"a": [1, 2], "b": 3, "c": [4, 5]}
    grid = generate_param_grid(params)
    expected = [
        {"a": 1, "b": 3, "c": 4},
        {"a": 1, "b": 3, "c": 5},
        {"a": 2, "b": 3, "c": 4},
        {"a": 2, "b": 3, "c": 5},
    ]
    assert grid == expected
