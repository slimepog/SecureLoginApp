from flask import Blueprint, request, session, jsonify, flash, redirect, url_for
from utils.crypto import hash_password, verify_password
from exceptions import *
from utils.validators import validate_password, validate_username
from models.user import create_user, check_user, get_user_by_username, user_exists, get_user_by_id
from utils.sessions import *

# sets the bp for all auth routes
auth_bp = Blueprint("auth", __name__, url_prefix="auth")





# handles register requests
@auth_bp.route("/register", methods=["POST"])
def register():
    new_username = request.form.get("username")
    new_password = request.form.get("password")

    try:
        
        if user_exists(new_username): # check if user exists 
            raise UsernameTaken() 
        validate_username(new_username) 
        validate_password(new_password) 
        create_user(new_username, new_password) # creates the user
        flash("User registered. Go To login page to log in to your account", "success")
        return redirect("/login_page")
    except Exception as e:
        flash(str(e), "error") # flashes the error accordingly
        return redirect("/register_page")


# handles login requests
@auth_bp.route("/login", methods= ["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    try:
        check_user(username, password) # validates the credentials
        start_user_session(username) # starts the users session
        return redirect("/welcome_page")
    except Exception as e:
        flash(str(e),"error") # flashes error accordingly
        return redirect("/login_page")

# handles logouts
@auth_bp.route("/logout", methods=["POST"])
def logout():
    end_user_session() # ends the users session
    return redirect("/login_page")



    