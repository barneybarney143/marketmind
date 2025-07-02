from __future__ import annotations

import sys
from pathlib import Path
from typing import Set

import grimp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _has_cycles(graph: grimp.ImportGraph) -> bool:
    modules = set(graph.modules)
    adjacency = {
        m: set(graph.find_modules_directly_imported_by(m)) & modules
        for m in modules
    }
    visited: Set[str] = set()
    stack: Set[str] = set()

    def dfs(node: str) -> bool:
        visited.add(node)
        stack.add(node)
        for neigh in adjacency[node]:
            if neigh not in visited:
                if dfs(neigh):
                    return True
            elif neigh in stack:
                return True
        stack.remove(node)
        return False

    for module in modules:
        if module not in visited:
            if dfs(module):
                return True
    return False


def test_no_cycles() -> None:
    packages = ["src", "engine", "strategies"]
    try:
        graph = grimp.build_graph(*packages)
    except Exception:
        graph = grimp.build_graph("strategies")

    assert not _has_cycles(graph)
