import sqlite3
from argon2 import PasswordHasher

# path to db
db_path = "dataBases/general.db"


# creates users db (remeber to handle permission levels)
def init_users_db():
    connection = sqlite3.connect(db_path)
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

# adds users to the db
# returns True or False based on if the username is taken or not
def add_user(username, password):
    connection = sqlite3.connect(db_path)
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

# basically here to validate login requests
# returns True or False based on if the login succeeded
# OFF COURSEE -> has to compare hashes and not plain text 
def check_user(username, password):
    connection = sqlite3.connect(db_path)
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

# ALWAYYSSSS USE argon2 ->>> best in the hash market (if even hash market exists)
# also this library always uses a random salt which is good i guess
def hash_password(password):
    ph = PasswordHasher()
    password_hashed = ph.hash(password)
    return password_hashed   


def init_chat_db():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()
    connection.close()

def add_conversation(message, bot_response, username):   
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO conversations (username, user_message, bot_response) VALUES (?, ?, ?)",
                    (username, message, str(bot_response)))
    connection.commit()
    connection.close()
# Python stuff 
if(__name__ == "__main__"):
    print("hello")