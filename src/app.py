from flask import Flask, render_template,redirect, session
from flask_socketio import SocketIO
import secrets
from config import Config

sockio = SocketIO()

def create_app():
    app = Flask(__name__)

    
    app.secret_key = Config.SECRET_KEY # sets key

    from utils.database import init_users_db, init_messages_db
    init_users_db()
    init_messages_db()

    from routes.auth import auth_bp
    from routes.chat import chat_bp
    from routes.main import main_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(chat_bp, url_prefix="/messages")
    app.register_blueprint(main_bp, url_prefix="/")

    sockio.init_app(app)
    return app

if __name__ == "__main__":
    from app import create_app, sockio
    app = create_app()
    sockio.run(app, host="127.0.0.1", port=5000, debug=True)




# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_socketio import SocketIO, emit, send
# import utils.database as database
# import sqlite3
# import secrets
# import string


# # Starts the app, session, db, and webSockets
# app = Flask(__name__)
# app.secret_key = secrets.token_urlsafe(32)
# database.init_users_db()
# database.init_chat_db()
# socketio = SocketIO(app)



# # just routes to the main page or if there is a session then it logs in
# @app.route("/")
# def home():
#     if "username" in session:
#         return redirect("/welcome_page")
#     return redirect("/login_page")

# #  login page 
# # NOTES FOR LATERRRR ----->>>>> maybe make design betterr
# @app.route("/login_page")
# def login_page():
#     return render_template("login.html")


# # gets login in params and verfies with the db
# # creates session if logged IN

# @app.route("/login", methods= ["POST"])
# def login():
#     username = request.form.get("username")
#     password = request.form.get("password")
#     success_logging_in = database.check_user(username, password)
#     if not success_logging_in:
#         flash("Invalid Username or Password.","error")
#         return redirect("/login_page")
#     session["username"] = username
#     return redirect("/welcome_page") 

    

    
    

# # Register page
# @app.route("/register_page", methods =["GET"])
# def register_page():
#     return render_template("register.html")


# # gets the new params for the user and sends a request to the db
# # also validates password (maybe improve pass validation) 
# # IMPORTANT - improve pass validation
# @app.route("/register", methods=["POST"])
# def register():

#     new_username = request.form.get("username")
#     if len(new_username) < 4 or " " in new_username:
#         flash("Username must be at Least 4 Characters long and must not contain spaces.", "error")
#         return redirect("/register_page")
    
#     new_password = request.form.get("password")
#     if not validate_password(new_password):
#         flash("Password must be 8 Characters Long, Must contain a letter and a special Character", "error")
#         return redirect("/register_page")
#     success_registering = database.add_user(new_username, new_password)
#     if not success_registering:
#         flash("Username Is Taken, Please pick a new username.", "error")
#         return redirect("/register_page")
#     flash("User registered. Go To login page to log in to your account", "success")
#     return redirect("/login_page")

# def validate_password(password):
#     if len(password) < 8:
#         return False
#     if not any(char.isdigit() for char in password):
#         return False
#     if not any(char in string.punctuation for char in password):
#         return False
#     return True

 

# @app.route("/logout", methods = ["GET"] )
# def logout():
#     check_if_logged_in()
#     session.clear()
#     return redirect("/login_page")


# @app.route("/chat_page",methods = ["GET"])
# def chat_page():
#     check_if_logged_in()
#     return render_template("chat.html")






# # Improve this and make individual session tokens
# def check_if_logged_in():
#     if "username" not in session:
#         flash("Please log in first", "error")
#         return redirect("/login_page")
    

# # WebSockets
# @socketio.on('connect')
# def socket_connect():
#     check_if_logged_in()
    
#     print(f'connected!, sid: {request.sid}')
#     emit('connect', {'data': 'connected','sid':request.sid})
     
    

# @socketio.on('disconnect')
# def socket_disconnect():
#     check_if_logged_in()
#     print("Closing Connection", request.sid)
#     emit('disconnected', {'data': 'disconnected','sid':request.sid})



# @socketio.on('message')
# def socket_message(client_message):
#     check_if_logged_in()
#     print("Sending the message", request.sid)
#     emit('message', {'data': client_message, 'sid': request.sid})





# # ADDED THIS FOR THE JOKES (jk)
# if __name__ == "__main__":
#     app.run(host= "127.0.0.1", port= 5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
