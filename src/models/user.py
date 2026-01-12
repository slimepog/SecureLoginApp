from utils.database import get_db
from exceptions import UsernameTaken, WrongPassword, UserNotFound
from utils.crypto import hash_password, verify_password
from base64 import b64encode

# logic - 
# checks if username is taken - raises UsernameTaken Exception
# inserts into db
def create_user(username, password):
        if user_exists(username):
             raise UsernameTaken()
        conn = get_db()
        cursor = conn.cursor()
        
        # returns tuple
        # hashed_password[0] - pw_hash
        # hashed_password[1] - salt
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash, password_salt) VALUES (?, ?, ?)",
            (username, hashed_password[0], hashed_password[1])
        )
        conn.commit()
        cursor.close()
        conn.close()




# gets user by username (return sqlite 3 row obj)
def get_user_by_username(username):
    conn = get_db()
    user_row = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()
    return user_row


# gets user by id (return sqlite 3 row obj)
def get_user_by_id(user_id):
    connection = get_db()
    user_row = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    connection.close()
    return user_row

# basically here to validate login requests
# compares hashes and request username
# raises exceptions based on the result
def check_user(username, password):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT password_hash, password_salt FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user is None:
        raise UserNotFound()
    if not verify_password(password, user['password_salt'], user['password_hash']):
        raise WrongPassword()

# check if user exists
def user_exists(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user is None:
        return False
    return True


# updates the users new uuid
def save_user_session_uuid(id, session_uuid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET active_session_uuid = ? WHERE id = ?", (session_uuid ,id))
    conn.commit()
    cursor.close()
    conn.close()


# clears the users uuid (usually on logout)
def clear_user_session_uuid(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET active_session_uuid = NULL WHERE id = ?", (id, ))
    conn.commit()
    cursor.close()
    conn.close()