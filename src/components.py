"""Reusable Streamlit UI components."""

from __future__ import annotations

import time
from collections.abc import Sequence

import streamlit as st

from src.parser import count_code_lines, detect_technologies


def show_progress(total: int, label: str) -> None:
    """Render an animated progress counter for a positive total."""
    metric, progress = st.empty(), st.empty()
    for current in range(0, total + 1, max(1, total // 100)):
        metric.metric(label=label, value=current)
        progress.progress(current / total if total else 1.0)
        time.sleep(0.005)
    metric.metric(label=label, value=total)
    progress.progress(1.0)


@st.fragment
def task_browser(tasks: Sequence[dict[str, object]]) -> None:
    """Render a filterable, stateful task browser from task dictionaries."""
    st.markdown("## Tasks viewer ")
    technology_column, search_column = st.columns([1, 2])
    with technology_column:
        selected_technology = st.selectbox("Technology:", ["All", "Pandas", "NumPy", "Scikit-Learn", "Regex", "OS", "Pathlib", "Pure Python"], key="filter_tech")
    filtered = [task for task in tasks if selected_technology == "All" or selected_technology in detect_technologies(str(task.get("solve", "")))]
    with search_column:
        query = st.text_input("Search in tasks or code", key="task_search").lower()
    if query:
        filtered = [task for task in filtered if query in str(task.get("content", "")).lower() or query in str(task.get("solve", "")).lower()]
    if not filtered:
        st.warning("Not Found")
        return
    st.session_state.setdefault("task_index", 0)
    st.session_state.task_index = min(st.session_state.task_index, len(filtered) - 1)
    previous, _, next_ = st.columns([1, 4, 1])
    with previous:
        if st.button("⬅️", disabled=st.session_state.task_index == 0, use_container_width=True):
            st.session_state.task_index -= 1
    with _:
        selected = st.slider("Choose task", 1, len(filtered), st.session_state.task_index + 1, label_visibility="collapsed")
        st.session_state.task_index = selected - 1
    with next_:
        if st.button("➡️", disabled=st.session_state.task_index == len(filtered) - 1, use_container_width=True):
            st.session_state.task_index += 1
    task = filtered[st.session_state.task_index]
    code = str(task.get("solve", ""))
    technologies = " • ".join(f"`{item}`" for item in detect_technologies(code))
    with st.container(border=True):
        left, right = st.columns([2, 1])
        left.markdown(f"### Task Prompt {st.session_state.task_index + 1} of {len(filtered)}")
        right.caption(f"🛠Technology {technologies} | Lines: `{count_code_lines(code)}`")
        st.divider()
        st.markdown(f"**Solve:**\n\n{task.get('content', '')}")
        st.markdown("##### Code:")
        st.code(code, language="python", line_numbers=True)
