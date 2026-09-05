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
end_date=datetime.datetime(2027, 1,1)
total_days=(end_date-start_date).days


task_number=0
result=[]

for nb in notebooks:
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            task_number += 1
            content = cell.source.replace("\n", " ")
            if total_tasks>1:
                fraction=task_number/(total_tasks-1)
            else:
                fraction=0

            base_days=int(fraction*total_days)

            actual_days = int(fraction * total_days)

            task_date=start_date+datetime.timedelta(days=actual_days)
            date_str = task_date.strftime("%Y-%m-%d")

            task_name = f"Zadanie {task_number}"

        else:
            solve = cell.source.strip()
            task_dict = {"task": task_name, "content": content, "solve": solve, "date": date_str}
            result.append(task_dict)



with open("tasks.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)












