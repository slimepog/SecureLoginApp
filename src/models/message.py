from exceptions import EmptyMessage
from utils.database import get_db
from utils.validators import validate_content



def send_message(data):
    sender_id = data['sender_id']
    content = data['content']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)", (
         sender_id, 1, content
    ))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_messages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT messages.content, users.username FROM messages JOIN users ON messages.sender_id = users.id")
    messages = cursor.fetchall()
    return messages
#  -------- for now it is one big chat ----------
# def send_message(data):
#     content = data['content']

#     sender_id = data['sender_id']
#     recv_id = data['recv_id']
#     connection = get_db()
#     cursor = connection.cursor()
#     cursor.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)", (
#         sender_id, recv_id, content
#     ))
#     connection.commit()
#     cursor.close()
#     connection.close()

# def get_messages_by_id(sender_id, recv_id):
#     connecton = get_db()
#     cursor = connecton.cursor()
#     cursor.execute(
#         "SELECT content, created_at FROM messages WHERE sender_id=? AND receiver_id=? ORDER BY created_at ASC",
#         (sender_id, recv_id)
#     )
#     messages = cursor.fetchall()
#     cursor.close()
#     connecton.close()
    
#     return messages
