from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from helloworld import say_hello


def test_say_hello() -> None:
    assert say_hello() == "Hello, world!"
