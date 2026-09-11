import datetime
import nbformat
import json
import random
import numpy as np

files=["Zadania.ipynb", 'Automotive_TASK.ipynb']
notebooks=[]

total_tasks=0

for file_path in files:
    nb=nbformat.read(file_path, as_version=4)
    notebooks.append(nb)
    total_tasks += sum(1 for cell in nb.cells if cell.cell_type == 'markdown')


start_date=datetime.datetime(2026, 1, 1)
end_date=datetime.datetime(2026, 12,15)
total_days=(end_date-start_date).days
months = [datetime.date(2026, m, 1) for m in range(1, 13)]
month_weights = [random.randint(5, 150) for _ in range(12)]

task_number=0
result=[]

for nb in notebooks:
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            task_number += 1
            content = cell.source.replace("\n", " ")
            task_name = f"Zadanie {task_number}"


            chosen_month_start = random.choices(months, weights=month_weights, k=1)[0]
            random_day = random.randint(1, 28)
            task_date = datetime.datetime(chosen_month_start.year, chosen_month_start.month, random_day)


            date_str = task_date.strftime("%Y-%m-%d")

        else:
            solve = cell.source.strip()
            task_dict = {"task": task_name, "content": content, "solve": solve, "date": date_str}
            result.append(task_dict)


result = sorted(result, key=lambda x: int(x['task'].split()[1]))


with open("tasks.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)












