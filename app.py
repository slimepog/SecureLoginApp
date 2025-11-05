from flask import Flask, render_template, request, redirect, url_for
from argon2 import PasswordHasher
app = Flask(__name__)



import sqlite3
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
    hashed_password = hash_password(request.form.get("password"))
    sucsess_logging_in = try_Logging_in(username , hashed_password)

    

def try_Logging_in(username, hashedpassword):
    conn = sqlite3.connect("general.db")

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
    username = request.form.get("username")
    password = request.form.get("password")
    hashed_password = hash_password(password)


# password Hasher - users aragon2 algorithm 
def hash_password(password):
    ph = PasswordHasher()
    password_hashed = ph.hash(password)
    return password_hashed

if __name__ == "__main__":
    app.run(debug=True)
