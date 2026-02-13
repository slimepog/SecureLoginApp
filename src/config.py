import os

# config
class Config:
    SECRET_KEY = os.urandom(32)
    DB_PATH = "../data/general.db"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Strict"