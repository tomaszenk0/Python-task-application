import json
import re
import time
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from matplotlib import cm

st.set_page_config(layout='wide')

#Adding data from json to code
@st.cache_data
def load_data():
    with open("tasks.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return data
#animate bar
def pasek(tasks,etykiety):
    licznik=st.empty()
    pasek=st.empty()
    skok=max(1,tasks//100)
    for i in range(0,tasks+1, skok):
        licznik.metric(label=etykiety, value=i)
        percent=i/tasks
        pasek.progress(percent)
        time.sleep(0.005)
    licznik.metric(label=etykiety, value=tasks)
    pasek.progress(1.0)
#Counting amount of tasks used with different libraries
def libraries(show=True):
    tasks = load_data()

    targets={
        'pandas':['pandas', 'pd'],
        'numpy':['numpy', 'np'],
        'sklearn':['sklearn', 'scikit'],
        're':['import re'],
        'os':['import os', 'os.', 'os.path'],
        'pathlib':['pathlib', 'path(']
    }
    counts={}
    for key, keywords in targets.items():
        counts[key]=sum(1 for z in tasks if any(kw in z.get('solve', '').lower() for kw in keywords))
    if show:
        pasek(counts['numpy'], "Zadania z wykorzystaniem Numpy")
        pasek(counts['pandas'], "Zadania z wykorzystaniem Pandas")
        pasek(counts['sklearn'], "Zadania z wykorzystaniem Scikit-Learn")
    return (counts['pandas'],
        counts['numpy'],
        counts['sklearn'],
        counts['re'],
        counts['os'],
        counts['pathlib'])

#Looking for libraries in python
def get_task_technologies(solve_code):
    code_lower = solve_code.lower()
    techs = []

    if "pandas" in code_lower or "pd." in code_lower:
        techs.append("Pandas")
    if "numpy" in code_lower or "np." in code_lower:
        techs.append("NumPy")
    if "sklearn" in code_lower or "scikit" in code_lower:
        techs.append("Scikit-Learn")
    if "import re" in code_lower or "re." in code_lower:
        techs.append("Regex")
    if "os." in code_lower or "import os" in code_lower:
        techs.append("OS")
    if "pathlib" in code_lower:
        techs.append("Pathlib")

    return techs if techs else ["Pure Python"]

#Counting lines of code
def line_code():
    tasks=load_data()
    result=sum(1 for task in tasks for line in task.get("solve", "").split('\n') if line.strip())
    pasek(result, "Ilość linijek kodu")

def count_code_lines(solve_code):
    lines=solve_code.split('\n')
    return sum(1 for line in lines if line.strip() !='')

tasks=load_data()
amount=len(tasks)

#Counting unique days
def days():
    days=load_data()
    dates=[]
    for i in days:
        dates.append(i['date'])
    unique_dates=list(set(dates))
    result=len(unique_dates)
    pasek(result, "Ilość dni")

#data with amount tasks in every months and days of week
@st.cache_data
def dict_days():
    days=load_data()
    dates=[]
    for i in days:
        dates.append(i['date'])
    pd_dates=pd.Series(dates)
    dict_dates=pd_dates.value_counts().to_dict()
    df=pd.DataFrame(list(dict_dates.items()), columns=['Data', 'Amount'])
    df['Data']=pd.to_datetime(df['Data'])
    df['Month']=df['Data'].dt.strftime('%B')
    df['day_of_week']=df['Data'].dt.day_name()
    return df

df_days=dict_days()

def labels():
    st.title("Wykresy z użyciem Matplotlib")
    p, n, s, re, os, path = libraries(show=False)
    category = ['Pandas', 'Numpy', 'SCLEARN', 'RE', 'OS', 'PATHLIB']
    values = [p, n, s, re, os, path]

    colors = cm.cool([0.5 + 0.4 * (i / len(category)) for i in range(len(category))])

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(9, 9))
    fig.patch.set_facecolor('#0e1117')
    for a in ax.flat:
        a.set_facecolor('#161b22')
        a.tick_params(colors='white')
        a.xaxis.label.set_color('white')
        a.yaxis.label.set_color('white')

    bars = ax[0, 0].bar(category, values, width=0.7, color=colors, edgecolor='white')
    ax[0, 0].bar_label(bars, padding=4, weight='bold', color='white')
    ax[0, 0].tick_params(axis='x', rotation=50)
    ax[0, 0].set_ylim(0, max(values) * 1.1)
    ax[0, 0].set_title("Wykres pionowy", fontsize=12, pad=12, fontweight='bold', color='white')

    bars = ax[0, 1].barh(category, values, color=colors, edgecolor='white')
    ax[0, 1].bar_label(bars, label_type='center', weight='bold', fontsize=10, color='black')
    ax[0, 1].set_title("Wykres poziomy", fontsize=12, pad=12, fontweight='bold', color='white')

    ax[1, 0].plot(category, values, marker='o', linestyle='-', color='#00d2ff')
    ax[1, 0].fill_between(range(len(category)), values, color='#00d2ff', alpha=0.25)
    ax[1, 0].set_title("Wykres Liniowy", fontsize=12, pad=12, fontweight='bold', color='white')
    for x, y in zip(category, values):
        ax[1, 0].text(x, y + 2, str(y), ha='left', va='bottom', weight='bold', color='white')
    ax[1, 0].grid(True, linestyle='--', alpha=0.3, color='gray')

    ax[1, 1].vlines(x=range(len(category)), ymin=0, ymax=values, color=colors, alpha=0.8, linewidth=2)
    ax[1, 1].scatter(range(len(category)), values, color=colors, s=120, zorder=3)
    ax[1, 1].set_xticks(range(len(category)))
    ax[1, 1].set_xticklabels(category, color='white')

    for x_idx, y_val in enumerate(values):
        ax[1, 1].text(x_idx, y_val + (max(values) * 0.03), str(y_val), ha='center', weight='bold', fontsize=10,
                      color='white')

    ax[1, 1].set_title("Lolipop", fontsize=12, pad=12, fontweight='bold', color='white')
    ax[1, 1].set_ylim(0, max(values) * 1.2)
    ax[1, 1].tick_params(axis='x', rotation=30)
    ax[1, 1].spines['top'].set_visible(False)
    ax[1, 1].spines['right'].set_visible(False)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, wspace=0.25)
    st.pyplot(fig,use_container_width=False)
    plt.close(fig)

    with st.expander(" Dowiedz się więcej: Techniczna analiza wykresów i interpretacja danych"):

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

@st.cache_data
def methods():
    all_words=[]
    for item in tasks:
        solve=item.get('solve', '')
        words=re.findall(r'\.(?!com|googleapis|txt\b)[a-zA-Z_][a-zA-Z0-9_]*', solve)
        all_words.extend(words)
    counter=Counter(all_words)
    top_words=counter.most_common(11)

    category=[]
    values=[]
    for w, i in top_words:
        category.append(w)
        values.append(i)
    df_words = pd.DataFrame({'Category': category, "Values": values})

    frames=[]
    steps=200
    for i in range(1, steps+1):
        factor=i/steps
        for word,val in zip(category, values):
            current_val = int(val * factor)
            frames.append({
                'Category': word,
                'Values': current_val,
                'Frame': i,
                'Text_Clean':str(current_val) if i==steps else ""
            })
    df_frames=pd.DataFrame(frames)

    return df_words, df_frames


def labels_with_plotly(data):
    st.title("Wykresy z użyciem Plotly")

    fig1=px.pie(data, names='Category', values='Values', title='1.Pie')
    fig1.update_traces(hovertemplate='%{label}-%{value}<extra></extra>', pull=[0.09 if i==0 else 0 for i in range(len(data))]
                       )
    fig2=px.treemap(data, path=['Category'], values='Values', title='2.Tree Map')
    fig2.update_traces(hovertemplate='%{percentRoot:.1%}<extra></extra>')
    fig3=px.pie(data, names='Category', values='Values', hole=0.5, title='3.Donut')
    fig4=px.bar(how_words_animated, x='Category', y='Values',range_y=[0,103], animation_frame='Frame', animation_group='Category',text='Text_Clean', title='4.Bar')
    fig4.update_yaxes(tick0=0,
                      dtick=10)
    fig4.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 0.02
    fig4.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 0.2
    fig4.update_layout(hovermode=False, sliders=[])

    col1, col2=st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4=st.columns(2)
    with col3:
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        st.plotly_chart(fig4, use_container_width=True)
    with st.expander(" Dowiedz się więcej: Techniczna analiza wykresów Plotly i interpretacja metod Pythona"):
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


def labels_with_seaborn():

    st.title("Wykresy z użyciem Seaborn")
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    fig.patch.set_facecolor('#0e1117')

    for ax in axes.flat:
        ax.set_facecolor('#161b22')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')

    sns.barplot(
        data=df_days, x='Month', y='Amount', order=month_order, estimator=sum, errorbar=None, palette='mako',
        ax=axes[0, 0]
    )
    axes[0, 0].set_title("1. Sum tasks in every month", color='white')
    axes[0, 0].tick_params(axis='x', rotation=45)

    sns.barplot(
        data=df_days, x='day_of_week', y='Amount', order=days_order, estimator=sum, errorbar=None, palette='viridis',
        ax=axes[0, 1]
    )
    axes[0, 1].set_title("2. Sum tasks in every day of week", color='white')
    axes[0, 1].tick_params(axis='x', rotation=45)

    sns.stripplot(data=df_days, x='day_of_week', y='Amount', order=days_order, palette='Set2', jitter=0.25,
                  ax=axes[1, 0])
    axes[1, 0].set_title("3. Pojedyncze sesje w dniach tygodnia", color='white')
    axes[1, 0].tick_params(axis='x', rotation=30)

    pivot_df = df_days.pivot_table(index="day_of_week", columns='Month', values='Amount', aggfunc='sum').reindex(
        index=days_order, columns=month_order).fillna(0)

    sns.heatmap(pivot_df, cmap="YlGnBu", annot=True, fmt=".0f", cbar=False, ax=axes[1, 1], annot_kws={"color": "white"})
    axes[1, 1].set_title("4. Heat Map", color='white')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4)
    col_left, col_center, col_right=st.columns([1,2,1])
    with col_center:
        st.pyplot(fig, use_container_width=False)

    plt.close(fig)
    with st.expander(" Dowiedz się więcej: Techniczna analiza wykresów Seaborn i interpretacja aktywności"):
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


st.title('Nauka z Pythonem')
st.markdown("""
Witaj na stronie, która jest zapisem mojej praktycznej nauki Pythona! Umieściłem tu zestawienie 
wszystkich zadań, które do tej pory przerobiłem.


---

###  Co tutaj znajdziesz?

* **Przekrój umiejętności:** Zadania od czystych podstaw języka, przez analizę danych (**NumPy**, **Pandas**), aż po modele uczenia maszynowego w **Scikit-Learn**.
* **Pełny kontekst:** Każde zadanie zawiera oryginalną treść oraz moje rozwiązanie.
* **Statystyki i postępy:** Wykresy pokazujące, nad czym pracowałem i jak rozkładała się moja praca w czasie.

---

### Jak to powstało? (Czyli kilka słów o zapleczu technicznym)

Cały ten projekt to nie tylko rozwiązane zadania, ale też mały ekosystem kodu, który stworzyłem wokół nich:

1. **Autorskie skrypty generujące:** Pliki i dane potrzebne do niektórych zadań stworzyłem od zera za pomocą własnych skryptów w Pythonie.
2. **Automatyczna konwersja:** Oryginalnie pracowałem w środowisku **Jupyter Notebook**. Aby sprawnie przenieść wszystko na stronę, napisałem skrypt, który wyciągnął treści i rozwiązania z notebooków `.ipynb` i przekształcił je w czysty format `.json`.
3. **Symulacja danych w czasie:** Ponieważ podczas nauki nie śledziłem dokładnie czasu wykonania każdego zadania, dodałem do struktur JSON pole z datą i wzbogaciłem je o parametry losowe. Dzięki temu mogłem zbudować dla Was realistyczne statystyki czasowe i wizualizacje trendów!


""")


#col1, col2, col3 = st.columns(3)
#with col1:
#    pasek(amount, "Ile zadań zrobiłem")
#with col2:
#    days()
#with col3:
#    line_code()



@st.fragment
def przegladarka_zadan():
    st.markdown("##  Przeglądarka Zadań")

    col_tech, col_search = st.columns([1, 2])

    with col_tech:
        technologies = ['All', 'Pandas', 'NumPy', 'Scikit-Learn', 'Regex', 'OS', 'Pathlib', 'Pure Python']
        chose_tech = st.selectbox("Technologia:", options=technologies, key='filter_tech')

    if chose_tech != 'All':
        filtered_tasks = [t for t in tasks if chose_tech in get_task_technologies(t.get("solve", ""))]
    else:
        filtered_tasks = tasks

    with col_search:
        search_query = st.text_input(" Szukaj w treści lub kodzie:", "", key="task_search")

    if search_query:
        filtered_tasks = [
            t for t in filtered_tasks
            if
            search_query.lower() in t.get("content", "").lower() or search_query.lower() in t.get("solve", "").lower()
        ]

    how_filtered = len(filtered_tasks)

    if how_filtered == 0:
        st.warning("Nie znaleziono zadań spełniających kryteria.")
        return

    if 'indeks' not in st.session_state:
        st.session_state.indeks = 0
    if st.session_state.indeks >= how_filtered:
        st.session_state.indeks = 0

    def previous():
        if st.session_state.indeks > 0:
            st.session_state.indeks -= 1

    def next():
        if st.session_state.indeks < how_filtered - 1:
            st.session_state.indeks += 1

    nav_col1, nav_col2, nav_col3 = st.columns([1, 4, 1])

    with nav_col1:
        st.button('⬅️', on_click=previous, disabled=(st.session_state.indeks == 0), use_container_width=True)

    with nav_col2:
        st.slider(
            'Wybierz zadanie',
            min_value=1,
            max_value=how_filtered,
            value=st.session_state.indeks + 1,
            key='slider_indeks',
            on_change=lambda: st.session_state.update({'indeks': st.session_state.slider_indeks - 1}),
            label_visibility="collapsed"
        )

    with nav_col3:
        st.button('➡️', on_click=next, disabled=(st.session_state.indeks == how_filtered - 1),
                  use_container_width=True)

    actual_task = filtered_tasks[st.session_state.indeks]
    solve_code = actual_task.get("solve", "")
    tech_list = get_task_technologies(solve_code)
    lines_count = count_code_lines(solve_code)
    tech_str = " • ".join([f"`{t}`" for t in tech_list])

    with st.container(border=True):
        meta_col1, meta_col2 = st.columns([2, 1])
        with meta_col1:
            st.markdown(f"### Zadanie {st.session_state.indeks + 1} z {how_filtered}")
        with meta_col2:
            st.caption(f"🛠 {tech_str} |  Lines: `{lines_count}`")

        st.markdown("---")

        st.markdown(f"**Treść:**\n\n{actual_task['content']}")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#####  Kod rozwiązania:")
        st.code(solve_code, language='python', line_numbers=True)


how_words=methods()[0]
how_words_animated=methods()[1]
przegladarka_zadan()
st.title("A teraz przejdźmy do statystyk")
st.markdown("Stworzyłem zestaw wykresów wykorzystując trzy biblioteki do wizualizacji danych. Każda biblioteka obejmuje inny zbiór danych i przedstawia różne typy wykresów. Poniżej jest także opis poszczególnych wykresów.")
tab1,tab2,tab3=st.tabs([
    "Wykresy Matplotlib",
    "Wykresy Plotly",
    "Wykresy Seaborn"
])
with tab1:
    labels()
with tab2:
    labels_with_plotly(how_words)
with tab3:
    labels_with_seaborn()


