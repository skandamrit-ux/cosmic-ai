
import uuid
import time

_tasks = {}

def create_task(name, payload=None):
    task_id = str(uuid.uuid4())
    _tasks[task_id] = {
        "id": task_id,
        "name": name,
        "payload": payload or {},
        "status": "queued",
        "created": time.time()
    }
    return _tasks[task_id]

def get_tasks():
    return list(_tasks.values())

def get_task(task_id):
    return _tasks.get(task_id)

def complete_task(task_id, result=None):
    if task_id in _tasks:
        _tasks[task_id]["status"] = "completed"
        _tasks[task_id]["result"] = result
    return _tasks.get(task_id)
