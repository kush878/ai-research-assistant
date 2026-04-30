import sqlite3


DB_PATH = "users.db"


def _add_column_if_missing(cursor, table, column, definition):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = {row[1] for row in cursor.fetchall()}

    if column not in columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    _add_column_if_missing(c, "users", "username", "TEXT")

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

def save_chat(user_email, chat_name, messages):
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "DELETE FROM chats WHERE user_email=? AND chat_name=?",
        (user_email, chat_name)
    )

    conn.commit()
    conn.close()
    
def rename_chat(user_email, old_name, new_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "UPDATE chats SET chat_name=? WHERE user_email=? AND chat_name=?",
        (new_name, user_email, old_name)
    )

    conn.commit()
    conn.close()
