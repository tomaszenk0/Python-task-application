"""Streamlit entry point for the Python learning analytics dashboard."""

from __future__ import annotations

import streamlit as st

from src.components import show_progress, task_browser
from src.data_loader import (
    build_date_summary,
    build_method_frames,
    count_unique_task_days,
    load_tasks,
)
from src.parser import count_technology_usage, count_total_code_lines
from src.visualizations import (
    create_matplotlib_figure,
    create_plotly_figures,
    create_seaborn_figure,
)

st.set_page_config(page_title="Learning Python", page_icon="🐍", layout="wide")


@st.cache_data
def load_dashboard_data() -> tuple[tuple[dict[str, object], ...], object, object]:
    """Load and cache task data plus DataFrames used by the dashboard."""
    tasks = load_tasks()
    return tasks, build_date_summary(tasks), build_method_frames(tasks)


tasks, date_summary, (methods, method_frames) = load_dashboard_data()
technology_counts = count_technology_usage(tasks)

st.title("Learning Python")
st.markdown("""Welcome to a dashboard documenting my practical Python learning journey. It contains an overview of all the exercises I have completed so far.

---

### What will you find here?

* **A cross-section of skills:** from language fundamentals and data analysis (**NumPy**, **Pandas**) to **Scikit-Learn**.
* **Full context:** every task includes its original description and solution.
* **Statistics and progress:** charts show the scope of learning and activity over time.

---



The project uses exercises from Python courses, while the website design, task solutions, their analysis, and visualisations are entirely my own.""")

task_count = len(tasks)
unique_day_count = count_unique_task_days(tasks)
total_code_lines = count_total_code_lines(tasks)

task_column, day_column, line_column = st.columns(3)
with task_column:
    show_progress(task_count, "Completed tasks")
with day_column:
    show_progress(unique_day_count, "Active days")
with line_column:
    show_progress(total_code_lines, "Lines of code")

task_browser(tasks)
st.title("Now, let's move on to the statistics")
st.markdown("I created a set of charts using three data-visualisation libraries.")
matplotlib_tab, plotly_tab, seaborn_tab = st.tabs(["Matplotlib charts", "Plotly charts", "Seaborn charts"])

with matplotlib_tab:
    st.title("Charts created with Matplotlib")
    st.pyplot(create_matplotlib_figure(technology_counts), use_container_width=False)
    with st.expander("Learn more: chart interpretation"):
        st.markdown("### 1. Chart type overview (Matplotlib)")

        col_tech1, col_tech2 = st.columns(2)

        with col_tech1:
            st.markdown(r"""
                    * **Vertical Bar Chart:** Used to quickly identify the leading technologies (`NumPy` and `Pandas`). It uses a dynamic $Y$-axis range (+10%), $50^\circ$ rotation of $X$-axis labels, and value labels above the bars (`bar_label`).
                    * **Area Chart:** A line chart with markers (`marker='o'`) and transparent filling (`fill_between`). It illustrates the distribution profile and the decline in scale (the *scree plot* effect) between the main tools and supporting libraries.
                    """)

        with col_tech2:
            st.markdown("""
                    * **Horizontal Bar Chart:** Makes technology names naturally readable from top to bottom without rotating your head, with value labels placed centrally inside the bars.
                    * **Lollipop Chart:** A hybrid of a scatter chart (`scatter`) and baseline lines (`vlines`). It is a minimalist alternative to a bar chart that reduces visual noise (*ink-to-data ratio*).
                    """)

        st.markdown("---")
        st.markdown("### 2. Data interpretation")

        col_data1, col_data2 = st.columns(2)

        with col_data1:
            st.markdown("""
                    ** Core technologies:**
                    The vast majority of tasks use **NumPy** (**157**) and **Pandas** (**154**). A difference of only three tasks indicates parallel development in linear algebra and tabular data analysis. **Scikit-Learn** (**32**) represents a step towards predictive modelling.
                    """)

        with col_data2:
            st.markdown("""
                    ** Automation and data engineering:**
                    The skill set is complemented by exercises involving regular expressions (**RE** – **22**), file structures (**PATHLIB** – **17**), and system operations (**OS** – **16**). The charts demonstrate mastery of a complete analyst workflow *pipeline*.
                    """)


with plotly_tab:
    st.title("Charts created with Plotly")
    pie, treemap, donut, animated_bar = create_plotly_figures(methods, method_frames)
    left, right = st.columns(2)
    left.plotly_chart(pie, use_container_width=True)
    right.plotly_chart(treemap, use_container_width=True)
    left, right = st.columns(2)
    left.plotly_chart(donut, use_container_width=True)
    right.plotly_chart(animated_bar, use_container_width=True)
    with st.expander("Learn more: method interpretation"):
        st.markdown("### 1. Chart types and applied techniques overview (Plotly Express)")

        col_tech1, col_tech2 = st.columns(2)

        with col_tech1:
            st.markdown("""
                    * **Pie Chart with a Pulled Slice (`px.pie` with the `pull` parameter):**
                      * **Description:** Shows the percentage share of individual methods in the entire set.
                      * **Technique:** The ranking leader (`.random` - 14%) is effectively pulled out to immediately draw the viewer's attention.

                    * **Treemap (`px.treemap`):**
                      * **Description:** A rectangular hierarchical visualisation where each tile's area is proportional to the frequency of a given method.
                      * **Benefit:** A strong alternative to pie charts that makes area comparisons easier (for example, it is easy to see the advantage of `.random` and `.array` over the rest).
                    """)

        with col_tech2:
            st.markdown("""
                    * **Donut Chart (`px.pie` with the `hole=0.5` parameter):**
                      * **Description:** A modified pie chart with a cut-out centre.
                      * **Benefit:** Improves interface readability (the *data-to-ink ratio*) and gives a more modern look while preserving the same percentage breakdown.

                    * **Animated Bar Chart (`px.bar` with `animation_frame`):**
                      * **Description:** An interactive bar chart of absolute values for individual keywords.
                      * **Technique:** Uses Plotly animation frames (`animation_frame`), adding dynamically growing bars and smooth user interaction with the slider.
                    """)

        st.markdown("---")
        st.markdown("### 2. Analysis of method usage and code calls")

        col_data1, col_data2 = st.columns(2)

        with col_data1:
            st.markdown("""
                    ** Data generation and array work (NumPy):**
                    * **Dominant methods:** The most frequent calls are `.random` (**103 times / 14%**) and `.array` (**88 times / 11.9%**).
                    * **Conclusion:** This shows a strong focus on independently creating test data, simulations, and working with multidimensional NumPy arrays.
                    """)

        with col_data2:
            st.markdown("""
                    ** Processing and I/O operations (Pandas & others):**
                    * **DataFrame operations:** Data-loading and structuring methods rank highly: `.csv` (**85**), `.read_csv` (**74**), `.DataFrame` (**71**), and `.set_option` (**60**).
                    * **Other elements:** The presence of `.append` (**59**), `.nan` (**53**), `.columns` (**49**), and `.seed` (**42**) demonstrates data-cleaning practices (handling missing `NaN` values) and experiment reproducibility (`seed`).
                    """)

with seaborn_tab:
    st.title("Charts created with Seaborn")
    left, center, right = st.columns([1, 2, 1])
    center.pyplot(create_seaborn_figure(date_summary), use_container_width=False)
    with st.expander("Learn more: activity interpretation"):
        st.markdown("### 1. Chart types and applied techniques overview (Seaborn)")

        col_tech1, col_tech2 = st.columns(2)

        with col_tech1:
            st.markdown("""
                            * **Monthly Bar Chart (`sns.barplot` / `countplot` with the `Blues_d` palette):** 
                              * **Description:** Distribution of the total number of completed tasks across all 12 months.
                              * **Technique:** A sequential color gradient emphasizes the chronological passage of time and work intensity.

                            * **Day of the Week Bar Chart (`sns.barplot` with the `Greens_d` palette):**
                              * **Description:** Aggregate summary of activity across individual days of the week (Monday through Sunday).
                              * **Benefit:** Helps verify whether learning was consistent or took place in short, sporadic bursts.
                            """)

        with col_tech2:
            st.markdown("""
                            * **Scatter Plot / Strip Plot (`sns.stripplot` / `scatterplot`):**
                              * **Description:** Displays individual study sessions mapped to days of the week, where the $Y$-axis indicates the number of tasks completed in a given session.
                              * **Technique:** Using distinct colors for each day of the week (`hue` categorization) reveals the clustering and frequency of sessions of specific sizes.

                            * **Time Matrix / Heatmap (`sns.heatmap` with `annot=True`):**
                              * **Description:** A two-dimensional matrix combining days of the week ($Y$-axis) with months ($X$-axis).
                              * **Technique:** Enabling numerical annotations (`annot=True`) alongside palettes like `viridis` / `YlGnBu` allows for the immediate identification of peak activity days (e.g., **20 tasks on a Sunday in August**).
                            """)

        st.markdown("---")
        st.markdown("### 2. Analysis of time trends and study habits")

        col_data1, col_data2 = st.columns(2)

        with col_data1:
            st.markdown("""
                            ** Seasonality and monthly activity peaks:**
                            * **Leaders:** The highest activity was recorded in **August** (over 80 tasks), **December**, and **November**.
                            * **Dips:** Noticeable declines occurred in **April** (lowest task count) and **February**, indicating scheduled breaks or periods of project-focused intensive study.
                            """)

        with col_data2:
            st.markdown("""
                            ** Weekly rhythm and records:**
                            * **Consistent habit:** The total volume of completed tasks across weekdays is fairly balanced (approx. 80–90 tasks per day), with a slight tilt toward weekends (**Saturday and Sunday**).
                            * **Peak intensity:** According to the heatmap, the single-day work intensity records occurred on a **Sunday in August (20 tasks)** and a **Friday in August (16 tasks)**.
                            """)