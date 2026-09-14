# Python Learning Tracker & Analytics Dashboard

[![CI Pipeline](https://github.com/tomaszenk0/Python-task-application/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/tomaszenk0/Python-task-application/actions/workflows/ci.yml)
[![Live app](https://img.shields.io/badge/Live%20app-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://python-task.streamlit.app)

An interactive Streamlit dashboard that turns a collection of Python learning exercises into clear, explorable progress insights. Browse completed tasks, inspect solutions, and discover patterns in technologies, code structure, and learning activity over time.

**Live demo:** [python-task.streamlit.app](https://python-task.streamlit.app) 

##  Features

- **Interactive task browser** — filter tasks by detected technology, search across task descriptions and solutions, and navigate through the learning archive.
- **Progress metrics** — track the total number of completed tasks, active learning days, and non-empty lines of solution code.
- **Technology analysis** — identify Python ecosystem usage in solutions, including Pandas, NumPy, Scikit-Learn, regular expressions, `os`, and `pathlib`.
- **Multi-library visual analytics** — explore the same dataset with Matplotlib, Seaborn, and interactive Plotly charts, including animated visualisations.
- **Reusable, testable logic** — data processing and code-analysis functions are separated from the Streamlit interface and covered by unit tests.
- **Continuous quality checks** — GitHub Actions runs Ruff linting and Pytest on pushes and pull requests.

## 🛠 Tech Stack

| Area | Tools |
| --- | --- |
| Application | Python, Streamlit |
| Data processing | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Quality assurance | Pytest, Ruff |
| Automation | GitHub Actions (CI) |

##  Project Architecture

The project uses a clean, modular structure with clear separation between data access, analysis, presentation, and verification.

```text
.
├── app.py                  # Streamlit application entry point and page composition
├── data/
│   └── tasks.json          # Learning-task dataset and solution archive
├── src/
│   ├── data_loader.py      # JSON loading, caching, and DataFrame preparation
│   ├── parser.py           # Code-text analysis and usage counters
│   ├── visualizations.py   # Matplotlib, Seaborn, and Plotly figure factories
│   └── components.py       # Reusable Streamlit UI components
├── tests/
│   └── test_logic.py       # Unit tests for framework-independent logic
├── .github/workflows/
│   └── ci.yml              # Automated linting and test workflow
└── requirements.txt        # Application and development dependencies
```

### Design principles

- Streamlit rendering is kept separate from data and analysis logic.
- Visualisation functions create and return figures instead of rendering UI directly.
- The data layer is cached to keep the dashboard responsive.
- Pure functions can be verified independently with Pytest.

##  Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/tomaszenk0/Python-task-application.git
cd Python-task-application
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

Open the local URL displayed by Streamlit in your browser.

##  Tests and Code Quality

Run the unit test suite:

```bash
pytest
```

Run the linter:

```bash
ruff check src/ app.py tests/
```

The CI workflow executes both checks automatically for pushes and pull requests targeting `main` or `master`.

## ️ Deployment

The dashboard is deployed with **Streamlit Community Cloud** and is available at [python-task.streamlit.app](https://python-task.streamlit.app).

The deployment uses the repository entry point (`app.py`) and installs dependencies from `requirements.txt`. Every update pushed to the connected branch can be deployed through Streamlit Community Cloud.

##  What This Project Demonstrates

- Practical Python programming and modular application design
- Data loading, transformation, aggregation, and caching
- Interactive dashboards and data storytelling
- Automated testing, linting, and continuous integration
- A documented, deployable portfolio project

