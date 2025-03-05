import re
from wtforms import ValidationError

class PasswordStrength:
    def __init__(self, message=None):
        if message is None:
            message = "Password must be betweeen 8 and 64 characters long, and include at least one uppercase letter, one lowercase letter, one digit, and one special character."
            self.message = message
    
    def __call__(self, form, field):
        password_data = field.data
        if not (8 <= len(password_data) <= 64):
            message = field.gettext("Password must be between 8 and 64 characters long.")
            raise ValidationError(message)
    
        if not re.search(r"[A-Z]", password_data):
            message = field.gettext("Password must contain at least one uppercase letter.")
            raise ValidationError(message)
    
        if not re.search(r"[a-z]", password_data):
            message = field.gettext("Password must contain at least one lowercase letter.")
            raise ValidationError(message)
        
        if not re.search(r"[0-9]", password_data):
            message = field.gettext("Password must contain at least one digit.")
            raise ValidationError(message)
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password_data):
            message = field.gettext("Password must contain at least one special character.")
            raise ValidationError(message)
        