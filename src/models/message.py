from exceptions import EmptyMessage
from utils.database import get_db
from utils.validators import validate_content

# --------NOTE--------
# for now it is one big chat
# add personalized vhat with specific people
# --------NOTE--------




# updates the messages db
# NOTE --->>> fix this
# update the recevier id from 1 
# change this logic to better one
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

# gets all messages from the db
# only gets the username and content
def get_all_messages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT messages.content, users.username FROM messages JOIN users ON messages.sender_id = users.id")
    messages = cursor.fetchall()
    return messages

