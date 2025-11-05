import sqlite3
from argon2 import PasswordHasher


db_name = "dataBases/general.db"

def init_db():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        is_active INTEGER NOT NULL DEFAULT 1,
        permission_level INTEGER NOT NULL DEFAULT 1
    )''')
    connection.commit()
    connection.close()

def addUser(username, password):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        connection.close()
        return False
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hash_password(password)))
    connection.commit()
    connection.close()
    return True


def checkUser(username, password):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    connection.close()
    if user is None:
        return False
    ph = PasswordHasher()
    try:
        ph.verify(user[0], password)
        return True
    except:
        return False


def hash_password(password):
    ph = PasswordHasher()
    password_hashed = ph.hash(password)
    return password_hashed    
if(__name__ == "__main__"):
    print("hello")