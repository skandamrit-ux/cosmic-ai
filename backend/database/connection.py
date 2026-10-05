import sqlite3
from pathlib import Path
from backend.config import DATABASE_PATH

def get_connection():
    path = Path(DATABASE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(path)

def init_db():
    with get_connection() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()

def save_conversation(message, response):
    with get_connection() as db:
        db.execute(
            "INSERT INTO conversations (message, response) VALUES (?, ?)",
            (message, response)
        )
        db.commit()
