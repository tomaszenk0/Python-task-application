"""Unit tests for Streamlit-independent application logic."""

from src.data_loader import count_unique_task_days
from src.parser import count_code_lines, count_technology_usage, count_total_code_lines, detect_technologies, extract_method_calls


def test_count_code_lines_ignores_blank_lines() -> None:
    """Blank lines must not increase the code-line metric."""
    assert count_code_lines("x = 1\n\n  \nprint(x)") == 2


def test_detect_technologies_returns_detected_library() -> None:
    """The detector recognises aliases and returns a human-friendly name."""
    assert detect_technologies("import numpy as np\nnp.array([1])") == ["NumPy"]


def test_detect_technologies_defaults_to_pure_python() -> None:
    """Code without supported library markers is labelled Pure Python."""
    assert detect_technologies("print('hello')") == ["Pure Python"]


def test_extract_method_calls() -> None:
    """The extractor returns dot-prefixed calls and ignores URL suffixes."""
    assert extract_method_calls("frame.head()\nexample.com") == [".head"]


def test_count_technology_usage() -> None:
    """Technology counters count solutions rather than individual mentions."""
    counts = count_technology_usage(({"solve": "pd.DataFrame()"}, {"solve": "print(1)"}))
    assert counts["Pandas"] == 1


def test_aggregate_code_and_date_metrics() -> None:
    """Aggregate metrics sum solution lines and deduplicate task dates."""
    tasks = ({"solve": "x = 1\n\nprint(x)", "date": "2026-01-01"}, {"solve": "pass", "date": "2026-01-01"})
    assert count_total_code_lines(tasks) == 3
    assert count_unique_task_days(tasks) == 1
