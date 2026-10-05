from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

FILES = {

"backend/core/__init__.py": "",
"backend/core/tasks/__init__.py": "",
"backend/core/tasks/task_manager.py": r'''
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
''',

"backend/core/context/__init__.py": "",
"backend/core/context/context_manager.py": r'''
class ContextManager:
    def build(self, message, memories=None):
        memories = memories or []
        return {
            "message": message,
            "memory": memories
        }
''',

"backend/core/tools/__init__.py": "",
"backend/core/tools/tool_registry.py": r'''
class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, function):
        self.tools[name] = function

    def list(self):
        return sorted(self.tools.keys())

    def execute(self, name, **kwargs):
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        return self.tools[name](**kwargs)
''',

"backend/research/__init__.py": "",
"backend/research/research_engine.py": r'''
class ResearchEngine:
    def plan(self, query):
        return {
            "success": True,
            "query": query,
            "steps": [
                "understand",
                "retrieve",
                "compare",
                "verify",
                "summarize"
            ]
        }
''',

"backend/coding/__init__.py": "",
"backend/coding/code_engine.py": r'''
class CodeEngine:
    def analyze(self, code):
        return {
            "success": True,
            "language": "unknown",
            "lines": len(code.splitlines()),
            "characters": len(code)
        }
''',

"backend/security/__init__.py": "",
"backend/security/audit/__init__.py": "",
"backend/security/audit/audit_log.py": r'''
import time

_events = []

def record(event, details=None):
    item = {
        "timestamp": time.time(),
        "event": event,
        "details": details or {}
    }
    _events.append(item)
    return item

def recent(limit=100):
    return _events[-limit:]
''',

"backend/runtime/__init__.py": "",
"backend/runtime/runtime_manager.py": r'''
import time
import platform
import os

START_TIME = time.time()

def info():
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "pid": os.getpid(),
        "uptime": round(time.time() - START_TIME, 2)
    }
''',

"backend/api/__init__.py": "",
"backend/api/system_api.py": r'''
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
''',

"backend/api/task_api.py": r'''
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
''',

"backend/ai/__init__.py": "",

"backend/config/runtime.json": json.dumps({
    "project": "COSMIC AI",
    "architecture": "local-first",
    "primary_provider": "gemini",
    "memory": "persistent",
    "automatic_memory_deletion": False,
    "future_providers": [
        "groq",
        "mistral",
        "openrouter",
        "replicate"
    ],
    "capabilities": [
        "chat",
        "memory",
        "research",
        "coding",
        "automation",
        "tools",
        "verification",
        "multimodal",
        "device_control"
    ]
}, indent=2),

"backend/tests/core_smoke.py": r'''
import requests

BASE = "http://127.0.0.1:8000"

checks = [
    "/api/health",
    "/api/status",
    "/api/routes",
    "/api/memory/count",
    "/api/providers",
    "/api/ai/gemini",
    "/api/runtime",
    "/api/system/full"
]

for path in checks:
    r = requests.get(BASE + path, timeout=10)
    print(path, r.status_code, r.text[:300])

print("COSMIC CORE SMOKE TEST COMPLETE")
'''
}

def write_preserving(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and target.read_text(errors="ignore").strip():
        backup = target.with_suffix(target.suffix + ".bak")
        if not backup.exists():
            backup.write_text(target.read_text(errors="ignore"))

    target.write_text(content)

for path, content in FILES.items():
    write_preserving(path, content)

print("=" * 60)
print("COSMIC FOUNDATION UPGRADE COMPLETE")
print("=" * 60)
print(f"Created/updated: {len(FILES)} components")
print()
print("CORE:")
print("  ✓ Runtime manager")
print("  ✓ Task manager")
print("  ✓ Context manager")
print("  ✓ Tool registry")
print("  ✓ Research engine foundation")
print("  ✓ Coding engine foundation")
print("  ✓ Security audit foundation")
print()
print("ARCHITECTURE:")
print("  ✓ Persistent memory preserved")
print("  ✓ Gemini remains primary AI")
print("  ✓ Future providers remain supported")
print("  ✓ No automatic memory deletion")
print("  ✓ Backup files created before upgrades")
print()
print("NEXT:")
print("  Restart COSMIC and run the smoke test.")
