from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import session, Blueprint, flash, request, session
from app import sockio
from models.message import send_message
from utils.validators import validate_content
from models.user import get_user_by_id
from utils.sessions import require_single_session

# sets the bp for all chat routes
chat_bp = Blueprint("messages", __name__)


# keeps track of online suers
online_users = {}

# handles initial connection to the socket
@sockio.on("connect")
@require_single_session   
def handle_connect():
    print("Connection established baby", request.sid)

# handles socket closing + removes user from online users
@sockio.on("disconnect")
@require_single_session   
def handle_disconnect():
    sid = request.sid
    username = online_users.pop(sid, None)
    print("Brudda disconnected", sid, username)

# handles joining the chat
@sockio.on("join")
@require_single_session   
def handle_join(data):

    username = data.get("username")
    online_users[request.sid] = username

    emit("system", {"msg": f"{username} joined the chat"}, broadcast=True)  

# handles messages (in main chat - I think)
@sockio.on("message")
@require_single_session   
def handle_message(data):

    try: 
        validate_content(data['content']) # checks content is not empty
    except Exception as e:
        flash(str(e), "error")
        return
    send_message(data) # saves the message
    sender = get_user_by_id(data["sender_id"])

    sender_username = sender["username"]
    data_sent = {"sender": sender_username,    "content": data['content']}
    emit("chat", data_sent, broadcast=True)

# handles private messages - (not in use now)
@sockio.on("private_message")
@require_single_session   
def handle_pm(data):
    target = data.get("to")
    emit("private_chat", data, room=target)

   