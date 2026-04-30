import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            chat_name TEXT,
            messages TEXT,
            UNIQUE(user_email, chat_name)
        )
    """)

    conn.commit()
    conn.close()

import sqlite3

def save_chat(user_email, chat_name, messages):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            chat_name TEXT,
            messages TEXT,
            UNIQUE(user_email, chat_name)
        )
    """)

    # Check old record
    c.execute(
        "SELECT messages FROM chats WHERE user_email=? AND chat_name=?",
        (user_email, chat_name)
    )

    row = c.fetchone()

    # If existing data and new data empty -> skip overwrite
    if row:
        old_messages = row[0]

        if messages == "[]" and old_messages not in ("[]", "", None):
            conn.close()
            return

        c.execute(
            "UPDATE chats SET messages=? WHERE user_email=? AND chat_name=?",
            (messages, user_email, chat_name)
        )

    else:
        c.execute(
            "INSERT INTO chats(user_email, chat_name, messages) VALUES(?,?,?)",
            (user_email, chat_name, messages)
        )

    conn.commit()
    conn.close()


def load_chats(user_email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
        SELECT chat_name, messages
        FROM chats
        WHERE user_email=?
        ORDER BY id DESC
    """, (user_email,))

    rows = c.fetchall()
    conn.close()

    return rows

def delete_chat(user_email, chat_name):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "DELETE FROM chats WHERE user_email=? AND chat_name=?",
        (user_email, chat_name)
    )

    conn.commit()
    conn.close()
    
def rename_chat(user_email, old_name, new_name):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "UPDATE chats SET chat_name=? WHERE user_email=? AND chat_name=?",
        (new_name, user_email, old_name)
    )

    conn.commit()
    conn.close()