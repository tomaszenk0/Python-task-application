"""Pure functions for analysing task solution code."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable

TECHNOLOGY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Pandas": ("pandas", "pd."),
    "NumPy": ("numpy", "np."),
    "Scikit-Learn": ("sklearn", "scikit"),
    "Regex": ("import re", "re."),
    "OS": ("import os", "os.", "os.path"),
    "Pathlib": ("pathlib", "path("),
}


def count_code_lines(solve_code: str) -> int:
    """Return the number of non-empty lines in a solution string."""
    return sum(1 for line in solve_code.splitlines() if line.strip())


def count_total_code_lines(tasks: Iterable[dict[str, object]]) -> int:
    """Return the combined number of non-empty solution lines in all tasks."""
    return sum(count_code_lines(str(task.get("solve", ""))) for task in tasks)


def detect_technologies(solve_code: str) -> list[str]:
    """Return technologies detected in solution code, or ``Pure Python``."""
    code_lower = solve_code.lower()
    technologies = [
        name
        for name, keywords in TECHNOLOGY_KEYWORDS.items()
        if any(keyword in code_lower for keyword in keywords)
    ]
    return technologies or ["Pure Python"]


def count_technology_usage(tasks: Iterable[dict[str, object]]) -> dict[str, int]:
    """Return how many task solutions mention each supported technology."""
    counts = {name: 0 for name in TECHNOLOGY_KEYWORDS}
    for task in tasks:
        detected = detect_technologies(str(task.get("solve", "")))
        for technology in counts:
            if technology in detected:
                counts[technology] += 1
    return counts


def extract_method_calls(solve_code: str) -> list[str]:
    """Extract dot-prefixed method or attribute names from solution code."""
    return re.findall(r"\.(?!com|googleapis|txt\b)[a-zA-Z_][a-zA-Z0-9_]*", solve_code)


def count_method_calls(tasks: Iterable[dict[str, object]], limit: int = 11) -> list[tuple[str, int]]:
    """Return the most common dot-prefixed calls across task solutions."""
    calls = [
        method
        for task in tasks
        for method in extract_method_calls(str(task.get("solve", "")))
    ]
    return Counter(calls).most_common(limit)
