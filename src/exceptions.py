# username taken exception
class UsernameTaken(Exception):
    def __init__(self, message="Username is Taken, please choose a different one."):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message

# password too short exception
class PasswordTooShort(Exception):
    def __init__(self, message="Password is too short, please choose a password longer than 8 characters."):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message

# username too short exception
class UsernameTooShort(Exception):
    def __init__(self, message="Username is too short, please choose a username longer than 4 characters."):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message

# Ilegal character in password exception
class IlegalCharacterInPassword(Exception):
    def __init__(self, message="Password contains ilegal character"):
        self.message = message
        super().__init__(self.message)    
    def __str__(self):
        return self.message

# Ilegal character in username exception
class IlegalCharacterInUsername(Exception):
    def __init__(self, message="Username contains ilegal character"):
        self.message = message
        super().__init__(self.message)    
    def __str__(self):
        return self.message

# ilegal username exception
class IllegalUsername(Exception):
    def __init__(self, message="Username may not contain spaces"):
        self.message = message
        super().__init__(self.message)  
    def __str__(self):
        return self.message

# no upper case letter in password exception
class NoUppercaseInPassword(Exception):
    def __init__(self, message="Password must contain an uppercase letter, a number and a special character"):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message

# no digit in password exception
class NoDigitInPassword(Exception):
    def __init__(self, message="Password must have at least one digit"):
        self.message = message
        super().__init__()
    def __str__(self):
        return self.message

# no special character in password exception 
class NoSpecialCharacterInPassword(Exception):
    def __init__(self, message="Password must have at least one special character"):
        self.message = message
        super().__init__()
    def __str__(self):
        return self.message

# User no found exception
class UserNotFound(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__()
    def __str__(self):
        return self.message

# Wrong password exception
class WrongPassword(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__()
    def __str__(self):
        return self.message

# Empty message exception
class EmptyMessage(Exception):
    def __init__(self, message="Cant send Empty messages"):
        self.message = message
        super().__init__()
    def __str__(self):
        return self.message
