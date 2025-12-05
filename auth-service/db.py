import sqlite3
from typing import Optional
from config import DB_FILE

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        loginId INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        hashedPassword TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(email: str, name: str, hashed_password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (email, name, hashedPassword) VALUES (?, ?, ?)",
        (email, name, hashed_password)
    )
    conn.commit()
    conn.close()

def update_user(email: str, field: str, new_value: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE users SET {field} = ? WHERE email = ?",
        (new_value, email)
    )
    conn.commit()
    conn.close()
