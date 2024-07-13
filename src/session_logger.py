import os
import sqlite3
from typing import Dict

from fastapi import HTTPException


def init_db():
    db_file = "connections.db"
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS connections (
                session_id TEXT PRIMARY KEY,
                username TEXT,
                password TEXT,
                host_name TEXT,
                database_name TEXT,
                port INTEGER,
                database_type TEXT
            )
        """
        )
        conn.commit()
        conn.close()


init_db()


def log_connection_details(session_id: str, data: Dict):
    conn = sqlite3.connect("connections.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO connections (session_id, username, password, host_name, database_name, port, database_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            session_id,
            data["username"],
            data["password"],
            data["host_name"],
            data["database_name"],
            data["port"],
            data["database_type"],
        ),
    )
    conn.commit()
    conn.close()


def fetch_connection_details(session_id: str) -> Dict:
    conn = sqlite3.connect("connections.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM connections WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "username": row[1],
            "password": row[2],
            "host_name": row[3],
            "database_name": row[4],
            "port": row[5],
            "database_type": row[6],
        }
    else:
        raise HTTPException(status_code=404, detail="Session ID not found")
