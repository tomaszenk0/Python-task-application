import streamlit as st
import json
import time
def load_data():
    with open("tasks.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return data
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
def libraries():
    tasks = load_data()
    numpy_tasks = [z for z in tasks if "numpy" in z['solve'].lower()]
    amount_n=len(numpy_tasks)
    pandas_tasks=[z for z in tasks if "pandas" in z['solve'].lower()]
    amount_p=len(pandas_tasks)
    scikit_lear_tasks = [z for z in tasks if "sklearn" in z['solve'].lower()]
    amount_s=len(scikit_lear_tasks)
    pasek(amount_n,"Zadania z wykorzystaniem Numpy")
    pasek(amount_p, "Zadania z wykorzystaniem Pandas")
    pasek(amount_s, "Zadania z wykorzystaniem Scikit-Learn")


def line_code():
    tasks=load_data()
    result=0
    for i in tasks:
        code = i.get("solve", "")
        code_lines = code.split('\n')
        for line in code_lines:
            if line.strip()!="":
                result+=1
    pasek(result, "Ilość linijek kodu")


tasks=load_data()
amount=len(tasks)


def days():
    days=load_data()
    dates=[]
    for i in days:
        dates.append(i['date'])
    unique_dates=list(set(dates))
    result=len(unique_dates)
    pasek(result, "Ilość dni")





st.title('Nauka z Pythonem')
st.markdown("""
Witaj na stronie, która jest zapisem mojej praktycznej nauki Pythona! Umieściłem tu zestawienie 
wszystkich zadań i projektów, które do tej pory przerobiłem.

Zamiast po prostu wrzucić pliki do folderu, postanowiłem podejść do sprawy jak na programistę przystało — 
**zbudować z nich interaktywny pulpit nawigacyjny**.

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

### A teraz przejdźmy do statystyk
""")
pasek(amount, "Ile zadań zrobiłem")
libraries()
line_code()
days()

@st.fragment
def przegladarka_zadan():
    if 'indeks' not in st.session_state:
        st.session_state.indeks = 0
    def previous():
        if st.session_state.indeks > 0:
            st.session_state.indeks -= 1

    def next():
        if st.session_state.indeks < amount - 1:
            st.session_state.indeks += 1



    actual_task=tasks[st.session_state.indeks]



    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.button('⬅️',
                  on_click=previous,
                  disabled=(st.session_state.indeks == 0))
    with col2:
        st.write(f'Zadanie {st.session_state.indeks + 1} z {amount}')

    with col3:
        st.button('➡️',
                  on_click=next,
                  disabled=(st.session_state.indeks == amount - 1))
    st.slider(
        '',
        min_value=0,
        max_value=amount-1,
        key='indeks'
    )

    st.write(actual_task['content'])
    st.write('Rozwiązanie')
    st.code(actual_task['solve'], language='python')

st.write('###   Podgląd Zadań')
przegladarka_zadan()

