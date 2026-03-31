"""
utils/chat_history.py
---------------------
SQLite-based backend for saving and loading chat history per mode.
Database file is stored at 'chat_logs/sgpa_history.db' (auto-created).
"""

import sqlite3
import os
from datetime import datetime

DB_DIR = "chat_logs"
DB_PATH = os.path.join(DB_DIR, "sgpa_history.db")


def _get_connection() -> sqlite3.Connection:
    """Creates the DB folder and returns a connection to the SQLite database."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows dict-like access to rows
    return conn


def init_db() -> None:
    """
    Creates the chat_history table if it doesn't exist yet.
    Call this once at app startup (e.g., in main.py).
    """
    conn = _get_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                mode      TEXT    NOT NULL,
                role      TEXT    NOT NULL,
                content   TEXT    NOT NULL,
                timestamp TEXT    NOT NULL
            )
        """)
    conn.close()


def save_message(mode: str, role: str, content: str) -> None:
    """
    Saves a single message to the database.

    Args:
        mode:    The current mode (e.g., "Explainer", "Summarizer", "Quizzer")
        role:    Either "user" or "assistant"
        content: The message text
    """
    conn = _get_connection()
    with conn:
        conn.execute(
            "INSERT INTO chat_history (mode, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (mode, role, content, datetime.now().isoformat(timespec="seconds"))
        )
    conn.close()


def load_history(mode: str) -> list[dict]:
    """
    Loads the full chat history for a given mode, oldest first.

    Returns:
        A list of dicts with keys: id, mode, role, content, timestamp.
        Returns an empty list if no history exists yet.
    """
    conn = _get_connection()
    cursor = conn.execute(
        "SELECT id, mode, role, content, timestamp FROM chat_history WHERE mode = ? ORDER BY id ASC",
        (mode,)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def clear_history(mode: str) -> None:
    """
    Deletes all saved messages for a given mode.
    Call this when the user clicks 'New Chat'.
    """
    conn = _get_connection()
    with conn:
        conn.execute("DELETE FROM chat_history WHERE mode = ?", (mode,))
    conn.close()


def clear_all_history() -> None:
    """Wipes the entire chat history across all modes."""
    conn = _get_connection()
    with conn:
        conn.execute("DELETE FROM chat_history")
    conn.close()


def get_all_modes_with_history() -> list[str]:
    """
    Returns a list of distinct modes that have saved messages.
    Useful for showing the user which past sessions exist.
    """
    conn = _get_connection()
    cursor = conn.execute("SELECT DISTINCT mode FROM chat_history")
    modes = [row["mode"] for row in cursor.fetchall()]
    conn.close()
    return modes
