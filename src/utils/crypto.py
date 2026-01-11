from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey
import os, base64

def hash_password(password: str) -> tuple[str,str]:
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=300_000,
        backend=default_backend()
    )
    key =kdf.derive(password.encode())

    return (base64.b64encode(key).decode(), base64.b64encode(salt).decode())

def verify_password(password: str, salt_b64: str, hash_b64: str) -> bool:
    salt = base64.b64decode(salt_b64)
    stored_key = base64.b64decode(hash_b64)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=300_000,
        backend=default_backend()
    )
    
    try:
        kdf.verify(password.encode(), stored_key)
    except InvalidKey:
        return False
    return True

def generate_token(length=32):
    return base64.urlsafe_b64encode(os.urandom(length)).decode()


    