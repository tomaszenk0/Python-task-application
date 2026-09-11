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
    pasek(amount_n,"Zadania z wykorzystaniem Numpy")
    pasek(amount_p, "Zadania z wykorzystaniem Pandas")

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




st.title('ZADANIA')
st.write('Statystyki zadań')
pasek(amount, "Ile zadań zrobiłem")
libraries()
line_code()
