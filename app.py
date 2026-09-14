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

Projekt korzysta z zadań z kursów Pythona ale projekt strony, rozwiązania zadań, ich analiza i wizualizacja są w pełni autorskie""")

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
        st.markdown("### 1. Przegląd Typów Wykresów (Matplotlib)")

        col_tech1, col_tech2 = st.columns(2)

        with col_tech1:
            st.markdown(r"""
                    * **Wykres Kolumnowy (Vertical Bar):** Służy do szybkiej identyfikacji liderów zestawienia (`Numpy` i `Pandas`). Zastosowano dynamiczny zakres osi $Y$ (+10%), rotację etykiet osi $X$ o $50^\circ$ oraz etykiety wartości nad słupkami (`bar_label`).
                    * **Wykres Liniowy z Wypełnieniem (Area Chart):** Wykres liniowy ze znacznikami (`marker='o'`) i przezroczystym wypełnieniem (`fill_between`). Obrazuje profil rozkładu i spadek skali (efekt *scree plot*) między głównymi narzędziami a bibliotekami pomocniczymi.
                    """)

        with col_tech2:
            st.markdown("""
                    * **Wykres Poziomy (Horizontal Bar):** Ułatwia naturalne czytanie nazw technologii od góry do dołu bez obracania głowy, z etykietami wartości umieszczonymi centralnie wewnątrz pasków.
                    * **Wykres Lizakowy (Lollipop Chart):** Hybryda wykresu punktowego (`scatter`) i linii bazowych (`vlines`). Minimalistyczny odpowiednik wykresu słupkowego, redukujący szum wizualny (*ink-to-data ratio*).
                    """)

        st.markdown("---")
        st.markdown("### 2. Merytoryczna Interpretacja Danych")

        col_data1, col_data2 = st.columns(2)

        with col_data1:
            st.markdown("""
                    ** Trzon technologiczny:**
                    Zdecydowaną większość stanowią zadania z **Numpy** (**157**) oraz **Pandas** (**154**). Różnica tylko 3 zadań wskazuje na równoległy rozwój w zakresie algebry liniowej oraz analizy danych tabelarycznych. **Scikit-Learn** (**32**) stanowi krok w stronę modelowania predykcyjnego.
                    """)

        with col_data2:
            st.markdown("""
                    ** Automatyzacja i Inżynieria Danych:**
                    Dopełnieniem umiejętności są zadania z wyrażeń regularnych (**RE** – **22**), struktury plików (**PATHLIB** – **17**) oraz operacji systemowych (**OS** – **16**). Wykresy dowodzą opanowania pełnego *pipeline'u* pracy analityka.
                    """)


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
        st.markdown("### 1. Przegląd Typów Wykresów i Zastosowanych Technik (Plotly Express)")

        col_tech1, col_tech2 = st.columns(2)

        with col_tech1:
            st.markdown("""
                    * **Wykres Kołowy z Wyciągniętym Wycinkiem (`px.pie` z parametrem `pull`):** 
                      * **Opis:** Pokazuje udział procentowy poszczególnych metod w całości zestawienia.
                      * **Technika:** Zastosowano efektywne wyciągnięcie (odsuniecie) lidera rankingu (`.random` - 14%), aby natychmiast przyciągnąć wzrok odbiorcy.

                    * **Treemap - Mapa Drzewa (`px.treemap`):**
                      * **Opis:** Prostokątna wizualizacja hierarchiczna, gdzie powierzchnia każdego kafelka jest proporcjonalna do częstości występowania danej metody.
                      * **Zaleta:** Świetna alternatywa dla wykresów kołowych, umożliwiająca prostszą wizualną porównywalność powierzchni (np. łatwe dostrzeżenie przewagi `.random` i `.array` nad resztą).
                    """)

        with col_tech2:
            st.markdown("""
                    * **Wykres Pierścieniowy (`px.pie` z parametrem `hole=0.5`):**
                      * **Opis:** Zmodyfikowany wykres kołowy z wyciętym środkiem (Donut Chart).
                      * **Zaleta:** Poprawia czytelność interfejsu (tzw. *data-to-ink ratio*), dając nowocześniejszy wygląd przy zachowaniu identycznego podziału procentowego.

                    * **Animowany Wykres Słupkowy (`px.bar` z `animation_frame`):**
                      * **Opis:** Interaktywny słupkowy wykres wartości bezwzględnych poszczególnych słów kluczowych.
                      * **Technika:** Wykorzystuje klatki animacji w Plotly (`animation_frame`), dodając element dynamicznego wzrostu słupków i płynnej interakcji użytkownika z suwakiem.
                    """)

        st.markdown("---")
        st.markdown("### 2. Merytoryczna Analiza Użycia Metod i Wywołań w Kodzie")

        col_data1, col_data2 = st.columns(2)

        with col_data1:
            st.markdown("""
                    ** Generowanie Danych i Praca z Tablicami (NumPy):**
                    * **Metody dominujące:** Najczęściej pojawiającymi się wywołaniami są `.random` (**103 razy / 14%**) oraz `.array` (**88 razy / 11.9%**). 
                    * **Wniosek:** Pokazuje to duży nacisk na samodzielne tworzenie danych testowych, symulacje oraz pracę na wielowymiarowych tablicach NumPy.
                    """)

        with col_data2:
            st.markdown("""
                    ** Przetwarzanie i Operacje I/O (Pandas & Inne):**
                    * **Operacje na ramkach danych:** Wysokie pozycje zajmują metody wczytywania danych i ich strukturyzacji: `.csv` (**85**), `.read_csv` (**74**), `.DataFrame` (**71**) oraz `.set_option` (**60**).
                    * **Inne składniki:** Obecność `.append` (**59**), `.nan` (**53**), `.columns` (**49**) i `.seed` (**42**) dowodzi praktyk z czyszczenia danych (obsługa braków `NaN`) oraz powtarzalności eksperymentów (`seed`).
                    """)

with seaborn_tab:
    st.title("Wykresy z użyciem Seaborn")
    left, center, right = st.columns([1, 2, 1])
    center.pyplot(create_seaborn_figure(date_summary), use_container_width=False)
    with st.expander("Dowiedz się więcej: interpretacja aktywności"):
        st.markdown("### 1. Przegląd Typów Wykresów i Zastosowanych Technik (Seaborn)")

        col_tech1, col_tech2 = st.columns(2)

        with col_tech1:
            st.markdown("""
                            * **Wykres Słupkowy Miesięczny (`sns.barplot` / `countplot` z paletą `Blues_d`):** 
                              * **Opis:** Rozkład łącznej liczby rozwiązanych zadań w podziale na 12 miesięcy.
                              * **Technika:** Zastosowanie sekwencyjnego gradientu kolorów podkreśla chronologiczny upływ czasu oraz intensywność pracy.

                            * **Wykres Słupkowy Dni Tygodnia (`sns.barplot` z paletą `Greens_d`):**
                              * **Opis:** Sumaryczne ujęcie aktywności w poszczególne dni tygodnia (od poniedziałku do niedzieli).
                              * **Zaleta:** Pozwala zweryfikować, czy nauka odbywała się w trybie ciągłym, czy miała charakter zrywny.
                            """)

        with col_tech2:
            st.markdown("""
                            * **Wykres Punktowy Rozproszony (`sns.stripplot` / `scatterplot`):**
                              * **Opis:** Przedstawia pojedyncze sesje naukowe przypisane do dni tygodnia, gdzie oś $Y$ określa liczbę zadań wykonanych podczas danej sesji.
                              * **Technika:** Zastosowanie odrębnych kolorów dla każdego dnia tygodnia (kategoryzacja `hue`) pozwala dostrzec zagęszczenie i powtarzalność sesji o określonej wielkości.

                            * **Mapa Czasowa / Heatmapa (`sns.heatmap` z `annot=True`):**
                              * **Opis:** Dwuwymiarowa macierz łącząca dni tygodnia (oś $Y$) z miesiącami (oś $X$).
                              * **Technika:** Włączenie adnotacji liczbowych (`annot=True`) oraz palety `viridis` / `YlGnBu` umożliwia natychmiastową lokalizację absolutnych rekordów dziennych (np. **20 zadań w niedzielę w sierpniu**).
                            """)

        st.markdown("---")
        st.markdown("### 2. Merytoryczna Analiza Trendów Czasowych i Nawyków Pracy")

        col_data1, col_data2 = st.columns(2)

        with col_data1:
            st.markdown("""
                            ** Sezonowość i Miesięczne Szczyty Aktywności:**
                            * **Liderzy:** Najwyższą aktywność odnotowano w **sierpniu** (ponad 80 zadań), **grudniu** oraz **listopadzie**. 
                            * **Spadki:** Wyraźne dołki widoczne są w **kwietniu** (najmniej zadań) oraz **lutym**, co wskazuje na okresowe przerwy lub intensywniejszą naukę w trybie projektowym/obozowym.
                            """)

        with col_data2:
            st.markdown("""
                            ** Rytm Tygodniowy i Rekordy:**
                            * **Stały nawyk:** Sumaryczna liczba zadań w dni tygodnia jest bardzo wyrównana (ok. 80–90 zadań dziennie), z lekką przewagą weekendów (**sobota i niedziela**).
                            * **Ekstremum:** Według Heatmapy absolutny rekord jednorazowego natężenia pracy przypada na **niedzielę w sierpniu (20 zadań)** oraz **piątek w sierpniu (16 zadań)**.
                            """)

