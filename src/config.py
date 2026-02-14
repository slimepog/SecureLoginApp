import os

# config
class Config:
    # flask stuff
    SECRET_KEY = os.urandom(32) # super important ->> in future add a permanent key to env variables
    DEBUG = False
    

    # db stuff
    DB_PATH = "data/general.db"
    
    # cookies stuff and protocols
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE= True
    SESSION_COOKIE_SAMESITE= "Strict"
    SESSION_COOKIE_MAX_AGE =3600  # 1 hour
    

    # password and username default settings
    PASSWORD_HASH_ITERATIONS =300_000
    PASSWORD_HASH_LENGTH= 32
    PASSWORD_HASH_SALT_LENGTH = 16
    PASSWORD_MIN_LENGTH = 8
    USERNAME_MIN_LENGTH =4

    # rate limit settings ---> should consider changing in future
    REGISTER_RATE_LIMIT ="5 per hour"
    LOGIN_RATE_LIMIT ="10 per hour"
    PAGE_RATE_LIMIT= "30 per hour"
    DEFAULT_RATE_LIMIT= "200 per day, 50 per hour"
    

    
    # https and hsts - mostly talisman stuff
    FORCE_HTTPS = True
    HSTS_MAX_AGE= 31536000  # 1 year
    HSTS_INCLUDE_SUBDOMAINS = True
    

    # referer policy - more talisman stuff
    REFERRER_POLICY = "strict-origin-when-cross-origin"
    

    # ----NOTE----
    # fix the console error regarding socketio script
    # ----NOTE----
    # csp stuff
    CSP_POLICY = {
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