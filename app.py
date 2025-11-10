from flask import Flask, render_template, request, redirect, url_for, flash, session
import chatbot as chat_bot_model
import database
import sqlite3
import secrets
import string


# Starts the app, session, and db
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
database.init_users_db()
database.init_chat_db()
chatbot = chat_bot_model.chatbot_init()


# just routes to the main page or if there is a session then it logs in
@app.route("/")
def home():
    if "username" in session:
        return redirect("/welcome_page")
    return redirect("/login_page")

#  login page 
# NOTES FOR LATERRRR ----->>>>> maybe make design betterr
@app.route("/login_page")
def login_page():
    return render_template("login.html")


# gets login in params and verfies with the db
# creates session if logged IN

@app.route("/login", methods= ["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    success_logging_in = database.check_user(username, password)
    if not success_logging_in:
        flash("Invalid Username or Password.","error")
        return redirect("/login_page")
    session["username"] = username
    return redirect("/welcome_page") 

    

    
    

# Register page
@app.route("/register_page", methods =["GET"])
def register_page():
    return render_template("register.html")


# gets the new params for the user and sends a request to the db
# also validates password (maybe improve pass validation) 
# IMPORTANT - improve pass validation
@app.route("/register", methods=["POST"])
def register():

    new_username = request.form.get("username")
    if len(new_username) < 4 or " " in new_username:
        flash("Username must be at Least 4 Characters long and must not contain spaces.", "error")
        return redirect("/register_page")
    
    new_password = request.form.get("password")
    if not validate_password(new_password):
        flash("Password must be 8 Characters Long, Must contain a letter and a special Character", "error")
        return redirect("/register_page")
    success_registering = database.add_user(new_username, new_password)
    if not success_registering:
        flash("Username Is Taken, Please pick a new username.", "error")
        return redirect("/register_page")
    flash("User registered. Go To login page to log in to your account", "success")
    return redirect("/login_page")

def validate_password(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in string.punctuation for char in password):
        return False
    return True

# Welcome page after logging in
@app.route("/welcome_page", methods = ["GET"])
def welcome():
    if "username" not in session:
        flash("Please log in first", "error")
        return redirect("/login_page")
    return render_template("welcome.html")

@app.route("/logout", methods = ["GET"] )
def logout():
    if "username" not in session:
        flash("Please log in first", "error")
        return redirect("/login_page")
    session.clear()
    return redirect("/login_page")


@app.route("/chat_page",methods = ["GET"])
def chat_page():
    if "username" not in session:
        flash("Please log in first", "error")
        return redirect("/login_page")
    return render_template("chat.html")



@app.route("/chat", methods=["POST"])
def chat():
    if "username" not in session:
        flash("Please log in first", "error")
        return redirect("/login_page")
    message = request.form.get("message")
    # response variable comes in as a json format of {"response": bot_response}, bot response already a string
    response = chat_bot_model.send_message_to_bot(message, chatbot, session["username"])
    return response
# ADDED THIS FOR THE JOKES (jk)
if __name__ == "__main__":
    app.run(host= "127.0.0.1", port= 5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
