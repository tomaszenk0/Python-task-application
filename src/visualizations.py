"""Chart factories.  They return figures and never render Streamlit UI."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
from matplotlib import cm
from matplotlib.figure import Figure
from plotly.graph_objects import Figure as PlotlyFigure


def create_matplotlib_figure(technology_counts: dict[str, int]) -> Figure:
    """Create the four-panel Matplotlib technology comparison figure."""
    categories = ["Pandas", "NumPy", "Scikit-Learn", "Regex", "OS", "Pathlib"]
    values = [technology_counts[name] for name in categories]
    maximum = max(values, default=1)
    colors = cm.cool([0.5 + 0.4 * index / len(categories) for index in range(len(categories))])
    fig, axes = plt.subplots(2, 2, figsize=(9, 9))
    fig.patch.set_facecolor("#0e1117")
    for axis in axes.flat:
        axis.set_facecolor("#161b22")
        axis.tick_params(colors="white")
        axis.xaxis.label.set_color("white")
        axis.yaxis.label.set_color("white")
    bars = axes[0, 0].bar(categories, values, width=0.7, color=colors, edgecolor="white")
    axes[0, 0].bar_label(bars, padding=4, weight="bold", color="white")
    axes[0, 0].tick_params(axis="x", rotation=50)
    axes[0, 0].set_ylim(0, maximum * 1.1)
    axes[0, 0].set_title("Wykres pionowy", fontweight="bold", color="white")
    bars = axes[0, 1].barh(categories, values, color=colors, edgecolor="white")
    axes[0, 1].bar_label(bars, label_type="center", weight="bold", color="black")
    axes[0, 1].set_title("Wykres poziomy", fontweight="bold", color="white")
    axes[1, 0].plot(categories, values, marker="o", color="#00d2ff")
    axes[1, 0].fill_between(range(len(categories)), values, color="#00d2ff", alpha=0.25)
    axes[1, 0].set_title("Wykres liniowy", fontweight="bold", color="white")
    axes[1, 0].grid(True, linestyle="--", alpha=0.3, color="gray")
    axes[1, 1].vlines(range(len(categories)), 0, values, color=colors, linewidth=2)
    axes[1, 1].scatter(range(len(categories)), values, color=colors, s=120)
    axes[1, 1].set_xticks(range(len(categories)), categories, rotation=30, color="white")
    axes[1, 1].set_ylim(0, maximum * 1.2)
    axes[1, 1].set_title("Lollipop", fontweight="bold", color="white")
    for index, value in enumerate(values):
        axes[1, 0].text(categories[index], value + 2, str(value), ha="left", color="white", weight="bold")
        axes[1, 1].text(index, value + maximum * 0.03, str(value), ha="center", color="white", weight="bold")
    axes[1, 1].spines["top"].set_visible(False)
    axes[1, 1].spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def create_plotly_figures(methods: pd.DataFrame, frames: pd.DataFrame) -> tuple[PlotlyFigure, PlotlyFigure, PlotlyFigure, PlotlyFigure]:
    """Create pie, treemap, donut, and animated bar Plotly figures."""
    pie = px.pie(methods, names="Category", values="Values", title="1. Pie")
    pie.update_traces(pull=[0.09 if index == 0 else 0 for index in range(len(methods))])
    treemap = px.treemap(methods, path=["Category"], values="Values", title="2. Tree Map")
    donut = px.pie(methods, names="Category", values="Values", hole=0.5, title="3. Donut")
    animated_bar = px.bar(frames, x="Category", y="Values", range_y=[0, 103], animation_frame="Frame", animation_group="Category", text="Text_Clean", title="4. Bar")
    animated_bar.update_yaxes(tick0=0, dtick=10)
    animated_bar.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 0.02
    animated_bar.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 0.2
    animated_bar.update_layout(hovermode=False, sliders=[])
    return pie, treemap, donut, animated_bar


def create_seaborn_figure(date_summary: pd.DataFrame) -> Figure:
    """Create monthly, weekly, session, and heat-map Seaborn charts."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    fig.patch.set_facecolor("#0e1117")
    for axis in axes.flat:
        axis.set_facecolor("#161b22")
        axis.tick_params(colors="white")
        axis.title.set_color("white")
    sns.barplot(data=date_summary, x="Month", y="Amount", order=months, estimator=sum, errorbar=None, palette="mako", ax=axes[0, 0])
    sns.barplot(data=date_summary, x="day_of_week", y="Amount", order=days, estimator=sum, errorbar=None, palette="viridis", ax=axes[0, 1])
    sns.stripplot(data=date_summary, x="day_of_week", y="Amount", order=days, palette="Set2", jitter=0.25, ax=axes[1, 0])
    pivot = date_summary.pivot_table(index="day_of_week", columns="Month", values="Amount", aggfunc="sum").reindex(index=days, columns=months).fillna(0)
    sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt=".0f", cbar=False, ax=axes[1, 1], annot_kws={"color": "white"})
    axes[0, 0].set_title("1. Sum tasks in every month", color="white")
    axes[0, 1].set_title("2. Sum tasks in every day of week", color="white")
    axes[1, 0].set_title("3. Pojedyncze sesje w dniach tygodnia", color="white")
    axes[1, 1].set_title("4. Heat Map", color="white")
    for axis in axes.flat:
        axis.tick_params(axis="x", rotation=40)
    fig.tight_layout()
    return fig
