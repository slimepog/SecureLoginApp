from flask import Flask, render_template,redirect, session, request
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
import secrets
from config import Config
import os
from flask_talisman import Talisman

# creates socketio object
sockio = SocketIO()


# -----NOTE-----
# ADD MORE LIMITS / SET DEFAULT LIMITS ----> UPDATE IN ROUTES
# ----NOTE------


#  init rate limiter
limiter = Limiter(
    key_func=get_remote_address, 
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://" #stores the current limit stats for each user on the python processes ram
)


# init csrf token object
csrf= CSRFProtect() 

# init app
def create_app():


    app = Flask(__name__)

    # ----NOTE----
    # fix the console error regarding socketio script
    # ----NOTE----
    
    # csp configuration
    csp = {
    'default-src': "'self'",
    'script-src': [
        "'self'",
        "https://cdn.socket.io/4.7.5/socket.io.min.js",
    ],
    'connect-src': ["'self'", "https://cdn.socket.io"],  # for websocks
    'style-src': ["'self'"],
    'img-src': ["'self'", "data:"],
    'object-src': "'none'",
    }

    Talisman(
        app,
        # hsts headers
        force_https=True,  
        strict_transport_security=True,
        strict_transport_security_max_age=31536000, # 1 year
        strict_transport_security_include_subdomains=True,
        # csp and csrf protocls
        referrer_policy='strict-origin-when-cross-origin', 
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src']
    )

    
    app.secret_key = Config.SECRET_KEY # sets key
    
    limiter.init_app(app) # enforces the rate limmiting
    csrf.init_app(app) # enforces csrf protection

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
    # off for now until i fix https issue
    base_dir = os.path.dirname(os.path.abspath(__file__))
    certs = (
        os.path.join(base_dir, "../certs/cert.pem"),
        os.path.join(base_dir, "../certs/key.pem")
    )
    # i need to turn ssl_context=certs
    sockio.run(app, host="127.0.0.1", port=5000, debug=True, ssl_context=certs)
