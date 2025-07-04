"""Simple hello world module."""

from __future__ import annotations


def say_hello(name: str = "World") -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}!"
