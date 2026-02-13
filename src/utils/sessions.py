from flask import session, redirect, url_for
from flask_socketio import emit
from secrets import token_hex
from models.user import save_user_session_uuid, get_user_by_id, clear_user_session_uuid, get_user_by_username
from functools import wraps

# starts the users session
# session holds 4 params
# user_id, username, logged_in, session_uuid
def start_user_session(username):
    user_row = get_user_by_username(username)
    session_uuid = token_hex(16) # generates random uuid

    session['user_id'] = user_row['id']
    session['username'] = user_row['username']  
    session['logged_in'] = True


    session["session_uuid"] = session_uuid

    save_user_session_uuid(user_row["id"], session_uuid) # overwrites uuid in db

# ends users sesions
def end_user_session():
    user_id = session.get("user_id")
    if user_id:
        clear_user_session_uuid(user_id)
    session.clear()

# returns based on if user is authenticated
def is_authenticated():
    return session.get('logged_in', False)

# returns based on if user is authenticated (helper func for decorator)
def is_socket_authenticated():
    # params
    user_id = session.get("user_id")
    session_uuid = session.get("session_uuid")
    logged_in = session.get("logged_in", False)
    
    # checks
    if not user_id or not session_uuid or not logged_in:
        return False
    user = get_user_by_id(user_id)
    if not user or session_uuid != user["active_session_uuid"]:
        return False
    
    return True

# kicks unauthorized users (helper func for decorator)
def handle_socket_unauthorized():
    if session.get("user_id"):
        end_user_session()
    emit("force_logout")

# socket authentication decorator 
def socket_authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # auth check
        if not is_socket_authenticated():
            handle_socket_unauthorized()
            return
        return f(*args, **kwargs)
    return wrapper

# decorator that checks if a users session exists and sends to login page if it doesnt
def require_single_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        session_uuid = session.get("session_uuid")

        if not user_id or not session_uuid:
            return redirect(url_for("main.login_page"))
        user = get_user_by_id(user_id)  

        if not user or session_uuid != user["active_session_uuid"]:
            end_user_session()
            return redirect(url_for("main.login_page"))
        
        return f(*args, **kwargs)
    return wrapper
    