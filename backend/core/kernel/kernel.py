from backend.ai.gateway.gateway import AIGateway
from backend.database.connection import save_conversation, get_connection
from backend.security.verification.verifier import verify_response

gateway = AIGateway()

def get_recent_history(limit=20):
    with get_connection() as db:
        rows = db.execute("""
            SELECT message, response
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    rows.reverse()

    history = []
    for message, response in rows:
        history.append({"role": "user", "content": message})
        history.append({"role": "model", "content": response})

    return history

def process_message(message):
    history = get_recent_history(10)

    result = gateway.chat(
        message,

        history=history
    )

    if not result.get("success"):
        return result

    response = result["message"]
    verified = verify_response(response)

    save_conversation(message, response)

    return {
        "success": True,
        "type": "response",
        "provider": result.get("provider"),
        "model": result.get("model"),
        "message": response,
        "verified": verified
    }
