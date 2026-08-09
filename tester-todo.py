import os
import time
import json

todo_request = "to-do-request.txt"
todo_response = "to-do-response.txt"
# ===================================
# BEGIN TO-DO MICROSERVICE OPERATIONS
# ===================================
def send_add_task():
    open(todo_request, "w").close()
    clear_screen()
    while True:
        task = input(f"What would you like to add to the todo list: ")
        if task.strip() == "":
            break
        else:
            user_input = input(f"Ok, is {task} correct? Press enter to confirm or cancel to restart")
        if user_input == "":
            break
        elif user_input.lower() == 'cancel':
            continue
        else:
            continue
    if task == '' or task == 'cancel':
        return
    else:
        request = {
                "action": "add",
                "task": task
            }
        with open(todo_request, 'w') as file:
            json.dump(request, file, indent=4)
    return

def send_remove_task():
    open(todo_request, "w").close()
    clear_screen()
    task_id = select_task_id()
    if task_id is None:
        return
    else:
        request = {
                "action": "remove",
                "id": int(task_id)
            }
        with open(todo_request, 'w') as file:
            json.dump(request, file, indent=4)
    return

    
def send_complete_task():
    open(todo_request, "w").close()
    clear_screen()
    task_id = select_task_id()
    if task_id is None:
        return
    else:
        request = {
                "action": "complete",
                "id": int(task_id)
            }
        with open(todo_request, 'w') as file:
            json.dump(request, file, indent=4)
    return

def format_tasks(tasks):
    if not tasks:
        return("Your To-DO list is empty") 
    formatted = "Your To:Do List:\n"
    for item in tasks:
        if item["done"]:
            status = 'x'
        else:
            status = " "
        formatted += f"[{status}] {item["id"]}. {item["task"]}\n"
    return formatted 

def get_tasks():
    time.sleep(1)
    with open(todo_response, "r") as file:
        current_tasks = json.loads(file.read())
    formatted = format_tasks(current_tasks)
    print(formatted)
    select_task_field()
    input('press enter to continue')
    return

def select_task_id():
    clear_screen()
    with open(todo_response, "r") as file:
        current_tasks = json.loads(file.read())
    formatted = format_tasks(current_tasks)
    print(formatted)
    while True:
        task_id = input(f"Which task would you like to select: ")
        if task_id.strip() == "":
            return None
        if task_id.lower() == 'cancel':
            return None
        if not task_id.isdigit():
            print("Please enter a valid task id \n")
            continue
        for item in current_tasks:
            if item["id"] == int(task_id):
                break
        else:
            print("Please enter a valid task id \n")
            continue

        user_input = input(f"Ok, is {task_id} correct? Press enter to confirm or cancel to restart: ")
        if user_input == "":
            return(int(task_id))
        elif user_input.lower() == 'cancel':
            continue
        else:
            continue

def select_task_field():
    while True:
        user_input = input(
            '1. Add task\n'
            '2. complete task\n'
            '3. delete task\n'
            'Pick a number for your correspoding request (or type cancel): ')
        if user_input.lower() == 'cancel':
            return
        if not user_input.isdigit():
            print ("Please select a valid field number \n")
            continue
        if user_input == "1":
            send_add_task()
            return
        if user_input == "2":
            send_complete_task()
            return
        if user_input == "3":
            send_remove_task()
            return
        else:
            print("Please select a valid category number")
            continue
        
# ===================================
# END TO-DO MICROSERVICE OPERATIONS
# ===================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear') 

if __name__ == "__main__":
    while True:
        get_tasks()