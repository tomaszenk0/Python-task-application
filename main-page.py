import streamlit as st
import json
import time
import matplotlib.pyplot as plt
import plotly.express as px
import re
from collections import Counter
import pandas as pd
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
def libraries(show=True):
    tasks = load_data()
    numpy_tasks = [z for z in tasks if "numpy" in z['solve'].lower()]
    amount_n=len(numpy_tasks)
    pandas_tasks=[z for z in tasks if "pandas" in z['solve'].lower()]
    amount_p=len(pandas_tasks)
    scikit_lear_tasks = [z for z in tasks if "sklearn" in z['solve'].lower()]
    amount_s=len(scikit_lear_tasks)
    re_tasks = [z for z in tasks if "import re" in z['solve'].lower()]
    amount_r = len(re_tasks)
    os_tasks = [z for z in tasks if ' os' in z['solve'].lower()]
    amount_os = len(os_tasks)
    path_tasks = [z for z in tasks if 'pathlib' in z['solve'].lower()]
    amount_path = len(path_tasks)

    if show:
        pasek(amount_n, "Zadania z wykorzystaniem Numpy")
        pasek(amount_p, "Zadania z wykorzystaniem Pandas")
        pasek(amount_s, "Zadania z wykorzystaniem Scikit-Learn")


    return amount_p, amount_n, amount_s, amount_r, amount_os, amount_path



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



def labels():
    p, n, s, re, os, path = libraries(show=False)
    category=['Pandas', 'Numpy', 'SCLEARN', 'RE', 'OS', 'PATHLIB']
    values=[p,n,s,re,os, path]

    fig,ax=plt.subplots(nrows=2, ncols=2, figsize=(13,15))

    bars=ax[0,0].bar(category, values, width=0.7 ,color='skyblue', edgecolor='black')
    ax[0,0].bar_label(bars, padding=4, weight='bold')
    ax[0,0].tick_params(axis='x', rotation=50)
    ax[0,0].set_ylim(0, max(values)*1.1 )

#drugi wykres
    bars= ax[0,1].barh(category, values, color='green',edgecolor='black')
    ax[0,1].bar_label(
        bars,
        label_type='center',
        weight= 'bold',
        fontsize=10
    )
#trzeci wykres
    ax[1,0].plot(category, values, marker='o', linestyle='-', color='green')
    for x,y in zip(category, values):
        ax[1,0].text(x, y+2, str(y), ha='left', va='bottom', weight='bold')
    ax[1,0].grid(True, linestyle='-', alpha=0.6, color='gray')

#czwarty wykres
    ax[1,1].scatter(category, values, color='blue')
    ax[1,1].grid(True, linestyle='-', alpha=0.6, color='gray')
    ax[1,1].invert_xaxis()
    for x,y in zip(category, values):
        ax[1,1].text(x,y+3, str(y), ha='center', weight='bold')

    st.pyplot(fig)




def methods():
    all_words=[]
    for item in tasks:
        solve=item.get('solve', '')
        words=re.findall(r'[a-z]+', solve)
        all_words.extend(words)
    counter=Counter(all_words)
    top_words=counter.most_common(11)

    category=[]
    values=[]
    for w, i in top_words:
        category.append(w)
        values.append(i)
    df_words = pd.DataFrame({'Category': category, "Values": values})

    #Klatki animacji
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
    fig1=px.pie(data, names='Category', values='Values', title='1.Pie')
    fig1.update_traces(hovertemplate='%{label}-%{value}<extra></extra>', pull=[0.09 if i==0 else 0 for i in range(len(data))]
                       )
    fig2=px.treemap(data, path=['Category'], values='Values', title='2.Tree Map')
    fig2.update_traces(hovertemplate='%{percentRoot:.1%}<extra></extra>')
    fig3=px.pie(data, names='Category', values='Values', hole=0.5, title='3.Donut')
    fig4=px.bar(how_words_animated, x='Category', y='Values',range_y=[0,800], animation_frame='Frame', animation_group='Category',text='Text_Clean', title='4.Bar')
    fig4.update_yaxes(tick0=0,
                      dtick=50)
    fig4.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 0.02
    fig4.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 0.2
    fig4.update_layout(hovermode=False)

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
#pasek(amount, "Ile zadań zrobiłem")
#libraries(show=True)
#line_code()
#days()

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
st.write('###   Wykresy')
labels()
how_words=methods()[0]
how_words_animated=methods()[1]
labels_with_plotly(how_words)

