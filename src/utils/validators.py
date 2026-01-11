import exceptions


def validate_password(password):
    if len(password) < 8:
        raise exceptions.PasswordTooShort()
    if not any(char.isdigit() for char in password):
        raise exceptions.NoDigitInPassword()
    if not any(char in """!#$%&*+-.?@^_~""" for char in password):
        raise exceptions.NoSpecialCharacterInPassword()
    if not any(char.isupper() for char in password):
        raise exceptions.NoUppercaseInPassword()
    if any(char in """"'(),/:;<=>""" for char in password):
        raise exceptions.IlegalCharacterInPassword()
    return True


def validate_username(username):
    if len(username) < 4:
        raise exceptions.UsernameTooShort()
    if any(char in """"'(),/:;<=>""" for char in username):
        raise exceptions.IlegalCharacterInUsername()
    return True
    
def validate_content(content):
    if not content:
        raise exceptions.EmptyMessage()