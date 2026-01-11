class UsernameTaken(Exception):
    def __init__(self, message="Username is Taken, please choose a different one."):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message

class PasswordTooShort(Exception):
    def __init__(self, message="Password is too short, please choose a password longer than 8 characters."):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message

class UsernameTooShort(Exception):
    def __init__(self, message="Username is too short, please choose a username longer than 4 characters."):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message


class IlegalCharacterInPassword(Exception):
    def __init__(self, message="Password contains ilegal character"):
        self.message = message
        super().__init__(self.message)    
    def __str__(self):
        return self.message

class IlegalCharacterInUsername(Exception):
    def __init__(self, message="Username contains ilegal character"):
        self.message = message
        super().__init__(self.message)    
    def __str__(self):
        return self.message

class IllegalUsername(Exception):
    def __init__(self, message="Username may not contain spaces"):
        self.message = message
        super().__init__(self.message)  
    def __str__(self):
        return self.message

class NoUppercaseInPassword(Exception):
    def __init__(self, message="Password must contain an uppercase letter, a number and a special character"):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message

class NoDigitInPassword(Exception):
    def __init__(self, message="Password must have at least one digit"):
        self.message = message
        super().__init__()
    def __str__(self):
        return self.message
        
class NoSpecialCharacterInPassword(Exception):
    def __init__(self, message="Password must have at least one special character"):
        self.message = message
        super().__init__()
    def __str__(self):
        return self.message

class UserNotFound(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__()
    def __str__(self):
        return self.message

class WrongPassword(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__()
    def __str__(self):
        return self.message

class EmptyMessage(Exception):
    def __init__(self, message="Cant send Empty messages"):
        self.message = message
        super().__init__()
    def __str__(self):
        return self.message
