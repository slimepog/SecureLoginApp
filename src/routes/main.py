from flask import Blueprint, redirect, session, render_template
from utils.sessions import is_authenticated, require_single_session
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@require_single_session   
def home():
    if is_authenticated():
        return redirect("/welcome_page")
    return redirect("/login_page")

#  login page 
# NOTES FOR LATERRRR ----->>>>> maybe make design betterr
@main_bp.route("/login_page")
def login_page():
    return render_template("login.html")

# Register page
@main_bp.route("/register_page", methods =["GET"])
def register_page():
    return render_template("register.html")

# Welcome page after logging in
@main_bp.route("/welcome_page", methods = ["GET"])
@require_single_session   
def welcome_page():
    return render_template("welcome.html")

@main_bp.route("/chat_page", methods= ["GET"])
@require_single_session   
def chat_page():
    return render_template("chat.html", username=session["username"], user_id=session["user_id"])
