"""Database helper functions for the Mini Bug Tracker (SQLite + parameterized SQL)."""
import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "database", "bug_tracker.db")


def get_db_path():
    """Return the DB path. Tests can override it with the BUG_TRACKER_DB env variable."""
    return os.environ.get("BUG_TRACKER_DB", DEFAULT_DB_PATH)


def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the bugs table if it does not exist."""
    os.makedirs(os.path.dirname(get_db_path()), exist_ok=True)
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS bugs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT NOT NULL,
            severity    TEXT NOT NULL,
            priority    TEXT NOT NULL,
            status      TEXT NOT NULL,
            tester_name TEXT NOT NULL,
            created_at  TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def insert_bug(title, description, severity, priority, status, tester_name):
    """INSERT a new bug and return its id."""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO bugs (title, description, severity, priority, status, tester_name, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, description, severity, priority, status, tester_name, created_at),
    )
    conn.commit()
    bug_id = cursor.lastrowid
    conn.close()
    return bug_id


def get_bugs(search="", status="", severity=""):
    """SELECT bugs, optionally filtered by title text, status and severity."""
    query = "SELECT * FROM bugs WHERE 1=1"
    params = []
    if search:
        query += " AND title LIKE ?"
        params.append("%" + search + "%")
    if status:
        query += " AND status = ?"
        params.append(status)
    if severity:
        query += " AND severity = ?"
        params.append(severity)
    query += " ORDER BY id DESC"
    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def get_bug_by_id(bug_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM bugs WHERE id = ?", (bug_id,)).fetchone()
    conn.close()
    return row


def update_bug_status(bug_id, new_status):
    """UPDATE the status of one bug."""
    conn = get_connection()
    conn.execute("UPDATE bugs SET status = ? WHERE id = ?", (new_status, bug_id))
    conn.commit()
    conn.close()


def count_bugs(status=None):
    """SELECT COUNT(*) for all bugs or for one status."""
    conn = get_connection()
    if status:
        count = conn.execute("SELECT COUNT(*) FROM bugs WHERE status = ?", (status,)).fetchone()[0]
    else:
        count = conn.execute("SELECT COUNT(*) FROM bugs").fetchone()[0]
    conn.close()
    return count
