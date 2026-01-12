from flask import Flask, render_template,redirect, session
from flask_socketio import SocketIO
import secrets
from config import Config

# creates SocketIO object
sockio = SocketIO()

# Initializes the app
def create_app():
    app = Flask(__name__)

    
    app.secret_key = Config.SECRET_KEY # sets key

    from utils.database import init_users_db, init_messages_db # starts users and messages db
    init_users_db()
    init_messages_db()

    from routes.auth import auth_bp
    from routes.chat import chat_bp
    from routes.main import main_bp
    # starts all 3 bp's
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(chat_bp, url_prefix="/messages")
    app.register_blueprint(main_bp, url_prefix="/")

    # hooks the app with sockets
    sockio.init_app(app)
    return app

# runs the app
if __name__ == "__main__":
    from app import create_app, sockio
    app = create_app()
    sockio.run(app, host="127.0.0.1", port=5000, debug=True)
