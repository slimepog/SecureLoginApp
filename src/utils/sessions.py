from flask import session

def start_user_session(user_row):
    session['user_id'] = user_row['id']
    session['username'] = user_row['username']
    session['logged_in'] = True

def end_user_session():
    session.clear()


def is_authenticated():
    return session.get('logged_in', False)