import streamlit as st
import json
import re
import pandas as pd
import plotly.express as px
from collections import Counter

# 1. KONFIGURACJA STRONY
st.set_page_config(
    page_title="Python Learning Analytics",
    page_icon="🐍",
    layout="wide"
)


# 2. KESZOWANIE I WCZYTYWANIE DANYCH (Szybkość działania)
@st.cache_data
def load_and_process_data():
    with open("tasks.json", "r", encoding="utf-8") as f:
        tasks = json.load(f)

    # Przetwarzanie i ekstrakcja metryk z kodu
    processed_tasks = []
    stop_words = {'in', 'def', 'return', 'for', 'import', 'from', 'as', 'if', 'else', 'none', 'true', 'false', 'and',
                  'or', 'not', 'with'}

    all_methods = []

    for idx, t in enumerate(tasks):
        code = t.get('solve', '')
        lines = [line for line in code.split('\n') if line.strip() != '']
        line_count = len(lines)

        # Ekstrakcja słów/metod z wykluczeniem słów kluczowych
        words = [w.lower() for w in re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)]
        filtered_words = [w for w in words if w not in stop_words and len(w) > 1]
        all_methods.extend(filtered_words)

        # Wykrywanie użytych bibliotek
        libs = []
        if 'pandas' in code.lower() or 'pd.' in code.lower(): libs.append('Pandas')
        if 'numpy' in code.lower() or 'np.' in code.lower(): libs.append('NumPy')
        if 'sklearn' in code.lower(): libs.append('Scikit-Learn')
        if 're' in code.lower(): libs.append('Regex')

        processed_tasks.append({
            'id': idx + 1,
            'task_name': t.get('task', f'Zadanie {idx + 1}'),
            'content': t.get('content', ''),
            'solve': code,
            'line_count': line_count,
            'libraries': libs if libs else ['Pure Python']
        })

    df = pd.DataFrame(processed_tasks)
    return df, Counter(all_methods)


df_tasks, method_counter = load_and_process_data()

# 3. NAGŁÓWEK I KPI
st.title("🐍 Portfolio Analytics: Python Codebase Inspector")
st.markdown("Aplikacja do automatycznej analizy statycznej i wizualizacji bazy rozwiązanych zadań programistycznych.")

st.divider()

# KARTY KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("Łącznie zadań", len(df_tasks))
col2.metric("Łącznie linii kodu", df_tasks['line_count'].sum())
col3.metric("Średnia długość kodu", f"{int(df_tasks['line_count'].mean())} linii")
col4.metric("Główna biblioteka", "Pandas")

st.divider()

# 4. INTERAKTYWNY DASHBOARD (PLOTLY)
st.subheader("📊 Analiza Technologiczna Bazy Zadań")

col_left, col_right = st.columns(2)

with col_left:
    # Rozkład wykorzystania bibliotek
    lib_series = df_tasks['libraries'].explode().value_counts().reset_index()
    lib_series.columns = ['Biblioteka', 'Liczba Zadań']

    fig_libs = px.bar(
        lib_series,
        x='Liczba Zadań',
        y='Biblioteka',
        orientation='h',
        title="Wykorzystanie Bibliotek w Zadaniach",
        color='Liczba Zadań',
        color_continuous_scale='Viridis'
    )
    fig_libs.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_libs, use_container_width=True)

with col_right:
    # Najczęstsze metody i funkcje
    top_words = pd.DataFrame(method_counter.most_common(10), columns=['Metoda/Słowo', 'Wystąpienia'])

    fig_words = px.treemap(
        top_words,
        path=['Metoda/Słowo'],
        values='Wystąpienia',
        title="Najczęściej Używane Konstrukcje i Metody",
        color='Wystąpienia',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_words, use_container_width=True)

st.divider()

# 5. PROFESJONALNA PRZEGLĄDARKA ZADAŃ Z FILTREM
st.subheader("🔍 Interaktywna Przeglądarka Zadań")

selected_lib = st.selectbox("Filtruj zadania po technologii:", ["Wszystkie"] + list(lib_series['Biblioteka']))

if selected_lib != "Wszystkie":
    filtered_df = df_tasks[df_tasks['libraries'].apply(lambda x: selected_lib in x)]
else:
    filtered_df = df_tasks

task_id = st.select_slider(
    "Wybierz numer zadania:",
    options=filtered_df['id'].tolist()
)

selected_task = filtered_df[filtered_df['id'] == task_id].iloc[0]

with st.expander(f"📌 Zadanie {selected_task['id']}: Szczegóły i Rozwiązanie", expanded=True):
    st.markdown(f"**Treść zadania:** {selected_task['content']}")
    st.markdown(
        f"**Użyte technologie:** `{', '.join(selected_task['libraries'])}` | **Liczba linii kodu:** `{selected_task['line_count']}`")
    st.code(selected_task['solve'], language="python")