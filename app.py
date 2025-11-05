from flask import Flask, render_template, request, redirect, url_for, flash, session
import database
import sqlite3
import secrets
import string



app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
database.init_db()


# ReRoutes the home page to the login page using redirect function
@app.route("/")
def home():
    return redirect(url_for("login_page"))

#  displays the login page - by returning the html
@app.route("/login_page")
def login_page():
    return render_template("login.html")


# handles login requests 
# currently only recieves two params:
# username - username
# password - password
# function logic should be as follows:
# recive packet -> input validation and sanitization-> hash -> 
# compare with database query -> if finds user than log in and if not then send message

@app.route("/login", methods= ["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    success_logging_in = database.checkUser(username, password)
    if not success_logging_in:
        flash("Invalid Username or Password.","error")
        return redirect("/login_page")
    session["username"] = username
    return redirect("/welcome_page") 

    

    
    

#  displays the register page - by returning the html
@app.route("/register_page", methods =["GET"])
def register_page():
    return render_template("register.html")


# handles register requests 
# currently only recieves two params:
# username - username
# password - password
# function logic should be as follows:
# recive packet -> validate username and password-> hash -> 
# enter into database -> send sucsess message
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
    success_registering = database.addUser(new_username, new_password)
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
    # Add a Welcome Page
    print("asd")
# password Hasher - users aragon2 algorithm 


if __name__ == "__main__":
    app.run(debug=True)
