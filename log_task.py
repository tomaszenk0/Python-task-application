import datetime
import json
def log_task(task_name, content):
    date=datetime.datetime.now()
    date=date.strftime("%Y-%m-%d")
    tasks = {"task": task_name, "content": content, "date": date}
    with open('tasks.json', 'a', encoding='utf-8')as f:
        json.dump(tasks, f)
        f.write("\n")

