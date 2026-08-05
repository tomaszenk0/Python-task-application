import datetime
import nbformat
import json
import random

nb=nbformat.read("Zadania.ipynb" , as_version=4)
content=""


total_tasks=sum(1 for cell in nb.cells if cell.cell_type=='markdown')

start_date=datetime.datetime(2026, 1, 1)
end_date=datetime.datetime(2026, 12,31)

total_days=(end_date-start_date).days
avg_step=total_days/max(total_tasks,1)

min_step=0
max_step=max(1, int(avg_step*1.8))

current_date=start_date

task_number=-1
result=[]
for cell in nb.cells:
    if cell.cell_type=="markdown":
        task_number+=1
        content=cell.source.replace("\n", " ")

        date_str = current_date.strftime("%Y-%m-%d")
        delta_days = random.randint(min_step, max_step)
        current_date += datetime.timedelta(days=delta_days)
        if current_date>end_date:
            current_date=end_date

        task_name = f"Zadanie {task_number}"

    else:
        solve= cell.source.strip()
        task_dict = {"task": task_name, "content": content, "solve": solve, "date": date_str}
        result.append(task_dict)

with open("tasks.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)












