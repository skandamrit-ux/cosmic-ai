from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.database.connection import init_db, get_connection
from backend.core.kernel.kernel import process_message
from backend.config import APP_NAME, APP_VERSION, HOST, PORT
import os, platform, time

app = Flask(__name__)
CORS(app)
init_db()
START_TIME = time.time()


@app.get("/")
def root():
    return jsonify({"success": True, "service": APP_NAME, "version": APP_VERSION, "status": "running"})


@app.get("/api/health")
def health():
    return jsonify({"success": True, "service": APP_NAME, "status": "healthy", "version": APP_VERSION})


# 1. Route discovery
@app.get("/api/routes")
def routes():
    return jsonify({
        "success": True,
        "routes": sorted([
            rule.rule for rule in app.url_map.iter_rules()
            if rule.rule != "/static/<path:filename>"
        ])
    })


# 2. COSMIC status
@app.get("/api/status")
def status():
    return jsonify({
        "success": True,
        "service": APP_NAME,
        "version": APP_VERSION,
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "platform": platform.system(),
        "python": platform.python_version()
    })


# 3. Memory count — READ ONLY
@app.get("/api/memory/count")
def memory_count():
    with get_connection() as db:
        count = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    return jsonify({"success": True, "count": count})


# 4. Conversation creation
@app.post("/api/conversations")
def create_conversation():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"success": False, "error": "message is required"}), 400
    return jsonify(process_message(message))


# 5. Memory search
@app.get("/api/memory/search")
def search_memory():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"success": False, "error": "q is required"}), 400

    with get_connection() as db:
        rows = db.execute(
            "SELECT id,message,response,created_at FROM conversations "
            "WHERE message LIKE ? OR response LIKE ? "
            "ORDER BY id DESC LIMIT 100",
            (f"%{q}%", f"%{q}%")
        ).fetchall()

    return jsonify({
        "success": True,
        "count": len(rows),
        "items": [
            {"id": r[0], "message": r[1], "response": r[2], "created_at": r[3]}
            for r in rows
        ]
    })


# 6. Paginated memory
@app.get("/api/memory/page")
def memory_page():
    try:
        page = max(1, int(request.args.get("page", 1)))
        limit = min(100, max(1, int(request.args.get("limit", 20))))
    except ValueError:
        return jsonify({"success": False, "error": "invalid page or limit"}), 400

    offset = (page - 1) * limit

    with get_connection() as db:
        rows = db.execute(
            "SELECT id,message,response,created_at FROM conversations "
            "ORDER BY id DESC LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()

    return jsonify({
        "success": True,
        "page": page,
        "limit": limit,
        "items": [
            {"id": r[0], "message": r[1], "response": r[2], "created_at": r[3]}
            for r in rows
        ]
    })


# 7. Read individual memory — NO DELETE
@app.get("/api/memory/<int:memory_id>")
def get_memory(memory_id):
    with get_connection() as db:
        row = db.execute(
            "SELECT id,message,response,created_at FROM conversations WHERE id=?",
            (memory_id,)
        ).fetchone()

    if not row:
        return jsonify({"success": False, "error": "memory not found"}), 404

    return jsonify({
        "success": True,
        "item": {
            "id": row[0],
            "message": row[1],
            "response": row[2],
            "created_at": row[3]
        }
    })


# 8. Gemini model information
@app.get("/api/ai/gemini")
def gemini_info():
    return jsonify({
        "success": True,
        "provider": "gemini",
        "configured": bool(os.getenv("GEMINI_API_KEY")),
        "model": os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    })


# 9. Runtime information
@app.get("/api/runtime")
def runtime():
    return jsonify({
        "success": True,
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "pid": os.getpid()
    })


# 10. Strict chat validation
@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "JSON object required"}), 400

    message = data.get("message")

    if not isinstance(message, str):
        return jsonify({"success": False, "error": "message must be a string"}), 400

    message = message.strip()

    if not message:
        return jsonify({"success": False, "error": "message cannot be empty"}), 400

    return jsonify(process_message(message))


@app.errorhandler(Exception)
def error_handler(error):
    return jsonify({
        "success": False,
        "error": str(error),
        "type": "server_error"
    }), 500


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)
