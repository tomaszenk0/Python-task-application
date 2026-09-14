"""Streamlit entry point for the Python learning analytics dashboard."""

from __future__ import annotations

import streamlit as st

from src.components import show_progress, task_browser
from src.data_loader import build_date_summary, build_method_frames, count_unique_task_days, load_tasks
from src.parser import count_technology_usage, count_total_code_lines
from src.visualizations import create_matplotlib_figure, create_plotly_figures, create_seaborn_figure


st.set_page_config(page_title="Nauka z Pythonem", page_icon="🐍", layout="wide")


@st.cache_data
def load_dashboard_data() -> tuple[tuple[dict[str, object], ...], object, object]:
    """Load and cache task data plus DataFrames used by the dashboard."""
    tasks = load_tasks()
    return tasks, build_date_summary(tasks), build_method_frames(tasks)


tasks, date_summary, (methods, method_frames) = load_dashboard_data()
technology_counts = count_technology_usage(tasks)

st.title("Nauka z Pythonem")
st.markdown("""Witaj na stronie, która jest zapisem mojej praktycznej nauki Pythona! Umieściłem tu zestawienie wszystkich zadań, które do tej pory przerobiłem.

---

### Co tutaj znajdziesz?

* **Przekrój umiejętności:** od podstaw języka, przez analizę danych (**NumPy**, **Pandas**), aż po **Scikit-Learn**.
* **Pełny kontekst:** każde zadanie zawiera oryginalną treść oraz rozwiązanie.
* **Statystyki i postępy:** wykresy pokazują zakres nauki i aktywność w czasie.

---

### Jak to powstało?

Projekt korzysta z autorskich skryptów generujących dane, konwersji notebooków Jupyter do JSON oraz symulowanych dat umożliwiających analizę trendów.""")

task_count = len(tasks)
unique_day_count = count_unique_task_days(tasks)
total_code_lines = count_total_code_lines(tasks)

task_column, day_column, line_column = st.columns(3)
with task_column:
    show_progress(task_count, "Ile zadań zrobiłem")
with day_column:
    show_progress(unique_day_count, "Ilość dni")
with line_column:
    show_progress(total_code_lines, "Ilość linijek kodu")

task_browser(tasks)
st.title("A teraz przejdźmy do statystyk")
st.markdown("Stworzyłem zestaw wykresów wykorzystujących trzy biblioteki do wizualizacji danych.")
matplotlib_tab, plotly_tab, seaborn_tab = st.tabs(["Wykresy Matplotlib", "Wykresy Plotly", "Wykresy Seaborn"])

with matplotlib_tab:
    st.title("Wykresy z użyciem Matplotlib")
    st.pyplot(create_matplotlib_figure(technology_counts), use_container_width=False)
    with st.expander("Dowiedz się więcej: interpretacja wykresów"):
        st.markdown("Wykresy kolumnowe, liniowe i lollipop porównują częstość wykorzystania bibliotek w rozwiązaniach.")

with plotly_tab:
    st.title("Wykresy z użyciem Plotly")
    pie, treemap, donut, animated_bar = create_plotly_figures(methods, method_frames)
    left, right = st.columns(2)
    left.plotly_chart(pie, use_container_width=True)
    right.plotly_chart(treemap, use_container_width=True)
    left, right = st.columns(2)
    left.plotly_chart(donut, use_container_width=True)
    right.plotly_chart(animated_bar, use_container_width=True)
    with st.expander("Dowiedz się więcej: interpretacja metod"):
        st.markdown("Wykresy pokazują ranking najczęstszych wywołań metod znalezionych w rozwiązaniach.")

with seaborn_tab:
    st.title("Wykresy z użyciem Seaborn")
    left, center, right = st.columns([1, 2, 1])
    center.pyplot(create_seaborn_figure(date_summary), use_container_width=False)
    with st.expander("Dowiedz się więcej: interpretacja aktywności"):
        st.markdown("Zestawienie przedstawia aktywność miesięczną, tygodniową oraz mapę intensywności pracy.")
