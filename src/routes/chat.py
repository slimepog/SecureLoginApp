from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask import session, Blueprint, flash, request
from app import sockio, limiter
from models.message import send_message
from utils.validators import validate_content
from models.user import get_user_by_id
from utils.sessions import socket_authenticated
# sets the bp for all chat routes
chat_bp = Blueprint("messages", __name__)


# keeps track of online users
# format - key: username, value: sid
online_users = {}

# handles initial connection to the socket
@sockio.on("connect")
@socket_authenticated
def handle_connect(data=None):
    print("Connection established: ", request.sid)

# handles socket closing + removes user from online users
@sockio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    username = None
    for key, value in online_users.items(): # finds the username in dict
        if value == sid:
            username = key
            break

    emit("system", {"msg": f"🔴 {username} left the chat"}, broadcast=True)
    
    print(f"Username: {username}, sid: {sid} disconnected")

# handles joining the chat
@sockio.on("join")
@socket_authenticated
def handle_join(data=None):
    username = session.get("username")
    online_users[username] = request.sid

    emit("system", {"msg": f"🟢 {username} joined the chat"}, broadcast=True)  

# handles messages (in main chat - I think)
@sockio.on("message")
@socket_authenticated
def handle_message(data):

    try: 
        validate_content(data['content']) # checks content is not empty
    except Exception as e:
        flash(str(e), "error")
        return
    
    sender_id = session.get("user_id")
    data['sender_id'] = sender_id
    send_message(data) # saves the message
    sender = get_user_by_id(sender_id)

    sender_username = sender["username"]
    data_sent = {"sender": sender_username,    "content": data['content']}
    emit("chat", data_sent, broadcast=True)

# handles private messages - (not in use now)
@sockio.on("private_message")
@socket_authenticated
def handle_pm(data):
    target = data.get("to")
    emit("private_chat", data, room=target)

# forces logout (triggers frontend)
def force_user_logout(username):
    sid = online_users.get(username)
    if sid:
        sockio.emit("force_logout", room=sid)