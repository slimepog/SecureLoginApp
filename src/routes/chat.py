from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import session, Blueprint, flash, request, session
from app import sockio
from models.message import send_message
from utils.validators import validate_content
from models.user import get_user_by_id
chat_bp = Blueprint("messages", __name__)



online_users = {}



@sockio.on("connect")
def handle_connect():
    print("Connection established baby", request.sid)

@sockio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    username = online_users.pop(sid, None)
    print("Brudda disconnected", sid, username)

@sockio.on("join")
def handle_join(data):

    username = data.get("username")
    online_users[request.sid] = username

    emit("system", {"msg": f"{username} joined the chat"}, broadcast=True)  

@sockio.on("message")
def handle_message(data):

    try: 
        validate_content(data['content'])
    except Exception as e:
        flash(str(e), "error")
        return
    send_message(data)
    sender = get_user_by_id(data["sender_id"])

    sender_username = sender["username"]
    data_sent = {"sender": sender_username,    "content": data['content']}
    emit("chat", data_sent, broadcast=True)

    
@sockio.on("private_message")
def handle_pm(data):
    target = data.get("to")
    emit("private_chat", data, room=target)