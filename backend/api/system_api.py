
from flask import Blueprint, jsonify
from backend.runtime.runtime_manager import info
from backend.core.tasks.task_manager import get_tasks
from backend.core.tools.tool_registry import ToolRegistry

system_api = Blueprint("system_api", __name__)
registry = ToolRegistry()

@system_api.get("/api/system/full")
def full_system():
    return jsonify({
        "success": True,
        "runtime": info(),
        "tasks": get_tasks(),
        "tools": registry.list()
    })
