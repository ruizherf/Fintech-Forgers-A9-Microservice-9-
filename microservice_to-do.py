import json
import os
import time

request_file = "to-do-request.txt"
response_file = "to-do-response.txt"
tasks_file = "todo_data.json"

def open_record():
    if os.path.getsize(tasks_file) == 0:
        return []
    with open(tasks_file, "r") as file:
        data = json.load(file)
    return data

def save_record(data):
    with open(tasks_file, "w") as file:
        json.dump(data, file, indent = 4)

def add_task(task):
    data = open_record()
    new_id = 0
    for item in data:
        if item["id"] > new_id:
            new_id = item['id']
    new_id += 1
    data.append({
        "id": new_id,
        "task": task,
        "done": False
    })
    save_record(data)
    open(request_file, "w").close()
    return ({
        "status": "success",
        "operation": "add_task",
        "id": new_id,
        "task": task
    })

def complete_task(task_id):
    data = open_record()
    for item in data:
        if item["id"] == task_id:
            item["done"]  = True
    save_record(data)
    open(request_file, "w").close()
    return ({
        "status": "success",
        "operation": "complete_task",
        "id": task_id
    })

def remove_task(task_id):
    data = open_record()
    new_data = []
    for item in data:
        if item["id"] != task_id:
            new_data.append(item)
    data = new_data.copy()
    save_record(data)
    open(request_file, "w").close()
    return ({
        "status": "success",
        "operation": "remove_task",
        "id": task_id
    })

def check_request():
    if os.path.getsize(request_file) == 0:
        return
    with open(request_file, "r") as file:
        current_request = json.loads(file.read())
    action = current_request.get("action")
    if action == "add":
        task = current_request.get("task")
        add_task(task)
    elif action == "complete":
        task_id = current_request.get("id")
        complete_task(task_id)
    elif action == "remove":
        task_id = current_request.get("id")
        remove_task(task_id)
    else:
        print(f"unknown action: {action}")
        open(request_file, "w").close()

def send_tasks():
    tasks = open_record()
    print(tasks)
    open(response_file, "w").close()
    with open(response_file, "w") as file:
        json.dump(tasks, file, indent = 4)

if __name__ == "__main__":
    while True:
        check_request()
        send_tasks()
        time.sleep(.2)