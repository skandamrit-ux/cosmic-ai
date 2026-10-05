
from flask import Blueprint, request, jsonify
from backend.core.tasks.task_manager import (
    create_task,
    get_tasks,
    get_task,
    complete_task
)

task_api = Blueprint("task_api", __name__)

@task_api.get("/api/tasks")
def tasks():
    return jsonify({
        "success": True,
        "items": get_tasks()
    })

@task_api.post("/api/tasks")
def create():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()

    if not name:
        return jsonify({
            "success": False,
            "error": "task name required"
        }), 400

    return jsonify({
        "success": True,
        "task": create_task(name, data.get("payload"))
    })

@task_api.get("/api/tasks/<task_id>")
def task(task_id):
    item = get_task(task_id)

    if not item:
        return jsonify({
            "success": False,
            "error": "task not found"
        }), 404

    return jsonify({
        "success": True,
        "task": item
    })

@task_api.post("/api/tasks/<task_id>/complete")
def complete(task_id):
    data = request.get_json(silent=True) or {}

    item = complete_task(
        task_id,
        data.get("result")
    )

    if not item:
        return jsonify({
            "success": False,
            "error": "task not found"
        }), 404

    return jsonify({
        "success": True,
        "task": item
    })
