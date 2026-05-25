# Example structure

tasks_db = []

def add_task(title, description, priority, due_date):
    task = {
        "id": len(tasks_db) + 1,
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }
    tasks_db.append(task)
    return task


def gettasks():
    return tasks_db


def search_tasks(query):
    return [t for t in tasks_db if query.lower() in t["title"].lower()]


def delete_task(task_id):
    global tasks_db
    tasks_db = [t for t in tasks_db if t["id"] != task_id]


def update_task(task_id, title, description, priority, due_date, completed):
    for task in tasks_db:
        if task["id"] == task_id:
            task["title"] = title
            task["description"] = description
            task["priority"] = priority
            task["due_date"] = due_date
            task["completed"] = completed
            return task