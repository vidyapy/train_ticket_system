def validate_username(username: str) -> str:
    if not username.isalnum():
        raise ValueError("Username must be alphanumeric")
    return username

def validate_password(password: str) -> str:
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long")
    return password

def validate_email(email: str) -> str:
    if "@" not in email:
        raise ValueError("Invalid email address")
    return email
