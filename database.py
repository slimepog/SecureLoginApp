import sqlite3


def innit_db():
    connection = sqlite3.connect("dataBases/general.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password_hash TEXT
                )''')
    connection.commit()
    connection.close()