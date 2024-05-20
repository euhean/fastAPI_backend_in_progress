import re
from datetime import datetime, timedelta


def verify_email(email: str) -> bool:
    pattern = r'^[a-zA-Z]+@[a-zA-Z]+\.[a-zA-Z]+$'
    return bool(re.match(pattern, email))


def verify_birthdate(birthdate: str) -> bool:
    try:
        birthdate_obj = datetime.strptime(birthdate, '%d/%m/%Y')
    except ValueError:
        return False
    
    today = datetime.today()
    age = today - birthdate_obj
    return age >= timedelta(days=18*365)


def verify_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not password.isalnum():  # Ensures no special characters
        return False
    return True


def verify_telephone(phone_number: str) -> bool:
    pattern = r'^\d{9}$'
    return bool(re.match(pattern, phone_number))
