from flask import Blueprint, request, session, jsonify, flash, redirect, url_for
from utils.crypto import hash_password, verify_password
from exceptions import *
from utils.validators import validate_password, validate_username
from models.user import create_user, check_user, get_user_by_username, user_exists, get_user_by_id
from utils.sessions import *
auth_bp = Blueprint("auth", __name__, url_prefix="auth")





# gets the new params for the user and sends a request to the db
# also validates password (maybe improve pass validation) 
# IMPORTANT - improve pass validation
@auth_bp.route("/register", methods=["POST"])
def register():

    new_username = request.form.get("username")
    new_password = request.form.get("password")

    try:
        
        if user_exists(new_username):
            raise UsernameTaken()
        validate_username(new_username)
        validate_password(new_password)
        create_user(new_username, new_password)
        flash("User registered. Go To login page to log in to your account", "success")
        return redirect("/login_page")
    except Exception as e:
        flash(str(e), "error")
        return redirect("/register_page")


# gets login in params and verfies with the db
# creates session if logged IN

@auth_bp.route("/login", methods= ["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    try:
        check_user(username, password)
        user = get_user_by_username(username)
        start_user_session(user)
        return redirect("/welcome_page")
    except Exception as e:
        flash(str(e),"error")
        return redirect("/login_page")

@auth_bp.route("/logout", methods=["POST"])
def logout():
    end_user_session()
    return redirect("/login_page")



    