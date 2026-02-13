import exceptions
from config import Config

# validates password - custom rules
# rules:
# longer than min chars, must have a digit, and spcial char, and not ilegal chars
def validate_password(password):
    if len(password) < Config.PASSWORD_MIN_LENGTH:
        raise exceptions.PasswordTooShort()
    if not any(char.isdigit() for char in password):
        raise exceptions.NoDigitInPassword()
    if not any(char in """!#$%&*+-.?@^_~""" for char in password):
        raise exceptions.NoSpecialCharacterInPassword()
    if not any(char.isupper() for char in password):
        raise exceptions.NoUppercaseInPassword()
    if any(char in """"'(),/:;<=> """ for char in password):
        raise exceptions.IlegalCharacterInPassword()
    return True

# validates username - custom rules
# rules:
# longer than 3 chars, no ilegal chars in it
def validate_username(username):
    if len(username) < Config.USERNAME_MIN_LENGTH:
        raise exceptions.UsernameTooShort()
    if any(char in """"'(),/:;<=> """ for char in username):
        raise exceptions.IlegalCharacterInUsername()
    return True

# validates content - checks if isnt empty 
def validate_content(content):
    if not content:
        raise exceptions.EmptyMessage()