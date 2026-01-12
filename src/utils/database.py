import sqlite3
from argon2 import PasswordHasher
from config import Config# path to db


# returns db connection object
def get_db():
    conn = sqlite3.connect(Config.DB_PATH)

    conn.row_factory = sqlite3.Row # rows are returned in a dictionary insted of list
    return conn

# creates users db (remeber to handle permission levels)
def init_users_db():
    connection = sqlite3.connect(Config.DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        password_salt TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        active_session_uuid TEXT,
        permission_level INTEGER NOT NULL DEFAULT 1
    )''')
    connection.commit()
    connection.close() 

# create chat db (maybe change the logic)
def init_messages_db():
    connection = sqlite3.connect(Config.DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER,
        receiver_id INTEGER,
        content TEXT,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        read_status INTEGER DEFAULT 0,
        FOREIGN KEY(sender_id) REFERENCES users(id),
        FOREIGN KEY(receiver_id) REFERENCES users(id)
    )
    ''')
    connection.commit()
    connection.close()

