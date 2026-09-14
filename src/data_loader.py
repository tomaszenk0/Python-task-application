"""I/O and DataFrame preparation functions, independent from Streamlit."""

from __future__ import annotations

import json
from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path

import pandas as pd

from src.parser import count_method_calls


DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


@lru_cache(maxsize=4)
def load_tasks(data_path: str | Path = DEFAULT_DATA_PATH) -> tuple[dict[str, object], ...]:
    """Load tasks from JSON and return an immutable, cached task collection."""
    with Path(data_path).open(encoding="utf-8") as file:
        raw_tasks = json.load(file)
    if not isinstance(raw_tasks, list):
        raise ValueError("The task data file must contain a JSON list.")
    return tuple(task for task in raw_tasks if isinstance(task, dict))


def build_date_summary(tasks: Sequence[dict[str, object]]) -> pd.DataFrame:
    """Aggregate task dates into a DataFrame for time-based charts."""
    dates = [str(task["date"]) for task in tasks if task.get("date")]
    date_counts = pd.Series(dates, dtype="object").value_counts()
    summary = pd.DataFrame({"Date": date_counts.index, "Amount": date_counts.values})
    summary["Date"] = pd.to_datetime(summary["Date"])
    summary["Month"] = summary["Date"].dt.strftime("%B")
    summary["day_of_week"] = summary["Date"].dt.day_name()
    return summary


def count_unique_task_days(tasks: Sequence[dict[str, object]]) -> int:
    """Return the number of distinct non-empty dates assigned to tasks."""
    return len({str(task["date"]) for task in tasks if task.get("date")})


def build_method_frames(tasks: Sequence[dict[str, object]], steps: int = 200) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create method-frequency data and animation frames for Plotly charts."""
    method_counts = count_method_calls(tasks)
    methods = pd.DataFrame(method_counts, columns=["Category", "Values"])
    frames = [
        {
            "Category": row.Category,
            "Values": int(row.Values * frame / steps),
            "Frame": frame,
            "Text_Clean": str(int(row.Values * frame / steps)) if frame == steps else "",
        }
        for frame in range(1, steps + 1)
        for row in methods.itertuples(index=False)
    ]
    return methods, pd.DataFrame(frames)
