import datetime
import nbformat
import json
import random
import re
nb=nbformat.read("Zadania.ipynb" , as_version=4)
content=""
current_date="01.01.2026"
current_date=datetime.datetime.strptime(current_date, ("%d.%m.%Y"))
task_number=-1
result=[]
for cell in nb.cells:
    if cell.cell_type=="markdown":
        date_str = current_date.strftime("%Y-%m-%d")
        task_number+=1
        content=cell.source.replace("\n", " ")
        delta_days = random.randint(0, 2)
        current_date += datetime.timedelta(days=delta_days)
        task_name = f"Zadanie {task_number}"

    else:
        solve= cell.source.strip()
        task_dict = {"task": task_name, "content": content, "solve": solve, "date": date_str}
        result.append(task_dict)

with open("tasks.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)










