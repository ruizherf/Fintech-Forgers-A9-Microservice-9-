To-Do JSON Microservice
=========================
Note: To run please run the microservice in a dedicated terminal prior to running the tester

Overview
--------
This microservice handles to-do list functions for the client by storing tasks in a JSON file (todo_data.json) in lieu of a database. It uses text pipelines to communicate with the client.

No other application imports or calls this microservice directly. All communications are done via text files that both the microservice and the client write to in order to communicate requests and information.

to-do-request.txt is used for receiving any requests from the client, such as adding, completing, or removing a task.

to-do-response.txt is used by the microservice for sending the current task list to the client.

Requesting Data
----------------
In order to request data from the microservice a request must be written to the to-do-request.txt file. Requests are written as a JSON object containing an "action" field and any additional fields the action requires.

Types of Requests:

Add - The client writes "add" for the action and includes the description of the task to be added.

example: send_add_task() prompts the user for a task description, then writes

    {"action": "add", "task": "Buy groceries"}

Complete - The client writes "complete" for the action and includes the id of the task to mark as done.

example: send_complete_task() prompts the user to select a task, then writes

    {"action": "complete", "id": 3}

Remove - The client writes "remove" for the action and includes the id of the task to delete.

example: send_remove_task() prompts the user to select a task, then writes

    {"action": "remove", "id": 3}


If the request file can only contain an of "action" value other than "add", "complete", or "remove" (or the field is missing). Otherwise no action is taken.

Receiving Data
--------------
This microservice simply writes the full current task list to to-do-response.txt on every loop cycle (roughly every 0.2 seconds). The client should read to-do-response.txt whenever it wants to display the current list of tasks to the user.

Example, based on the current stored data:

    [
        {"id": 1, "task": "Carwash", "done": True},
        {"id": 3, "task": "Clean", "done": False}
    ]

Client Interface
-----------------
The client presents a simple text menu (select_task_field()) with three options:

    1. Add task
    2. Complete task
    3. Delete task

Selecting an option calls the corresponding function, which clears to-do-request.txt, walks the user through entering (and confirming) the needed information, and writes the resulting request. Formatting of the To-Do list must be done on the client side. 

UML sequence diagram

    Client              to-do-request.txt      TodoService          to-do-response.txt
       |                       |                     |                       |
       |--write request------->|                     |                       |
       |                       |                     |                       |
       |                       |<--check_request()---|                       |
       |                       |                     |  add/complete/remove  |
       |                       |                     |  _task()              |
       |                       |                     |--send_tasks(list)---->|
       |                       |                     |                       |
       |<--------------------read response----------------------------------|
       |                       |                     |  (repeats every 0.2s) |

Known Issues
------------
- An unrecognized or missing "action" is only logged to the microservice's console (via print).

This is a proof of concept that requests to add, complete, and remove tasks can be received and reflected in the response; later versions will address these issues.
