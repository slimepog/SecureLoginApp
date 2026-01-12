from flask import session, redirect, url_for
from secrets import token_hex
from models.user import save_user_session_uuid, get_user_by_id, clear_user_session_uuid
from functools import wraps

def start_user_session(user_row):

    session_uuid = token_hex(16)

    session['user_id'] = user_row['id']
    session['username'] = user_row['username']  
    session['logged_in'] = True


    session["session_uuid"] = session_uuid

    save_user_session_uuid(user_row["id"], session_uuid)

def end_user_session():
    user_id = session["user_id"]
    clear_user_session_uuid(user_id)
    session.clear()


def is_authenticated():
    return session.get('logged_in', False)


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
    