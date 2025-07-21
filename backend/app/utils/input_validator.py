from marshmallow import validate
from app.utils.error_handler import APIError
from app.shared_constants.gender import gender_tuple

def username_validator(username: str) -> str:
    username = username.strip()
    if not validate.Length(min=4)(username):
        raise APIError(
            status=422,
            pointer="input_validator.py",
            title="Unprocessable Content: Username Format",
            detail="Username must be more than 4 characters.",
        )
    if not validate.Regexp(r'^[a-z0-9_-]+$')(username):
        raise APIError(
            status=422,
            pointer="input_validator.py",
            title="Unprocessable Content: Username Format",
            detail="Username must only contain lowercase letters, numbers, hyphens, and underscores.",
        )
    return username

def email_validator(email: str) -> str:
    email = email.strip()
    if not validate.Regexp(r'^[-.\w]+@[-.\w]+\.[-.\w]{2,}$')(email):
        raise APIError(
            status=422,
            pointer="input_validator.py",
            title="Unprocessable Content: Email Format",
            detail="Email needs to be in correct format",
        )
    return email

def password_validator(password: str) -> str:
    password = password.strip()
    if not validate.Length(min=8)(password):
        raise APIError(
            status=422,
            pointer="input_validator.py",
            title="Unprocessable Content: Password Format",
            detail="Password must be more than 8 characters long.",
        )
    if " " in password:
        raise APIError(
            status=422,
            pointer="input_validator.py",
            title="Unprocessable Content: Password Format",
            detail="Password should not contain spaces.",
        )
    if not validate.Regexp(r'[a-zA-Z0-9]')(password):
        raise APIError(
            status=422,
            pointer="input_validator.py",
            title="Unprocessable Content: Password Format",
            detail="Password must contain at least one alphanumeric character.",
        )
    return password

def name_validator(name: str) -> str:
    name = name.strip()
    if not validate.Regexp(r'^[a-zA-Z0-9\s]{2,}$')(name):
        raise APIError(
            status=422,
            pointer="input_validator.py",
            title="Unprocessable Content: Name Format",
            detail="Name must be at least 2 alphanumeric characters long.",
        )
    return name

def gender_validator(gender: str) -> str:
    if not validate.OneOf(gender_tuple)(gender):
        raise APIError(
            status=422,
            pointer="input_validator.py",
            title="Unprocessable Content: Gender",
            detail="Gender must be one of the available options.",
        )
    return gender


def phone_number_validator(phone_number: str) -> str:
    phone_number = phone_number.strip()
    if not validate.Regexp(r'^\+?[1-9](?:\s?\d){6,14}$')(phone_number):
        raise APIError(
            status=422,
            pointer="input_validator.py",
            title="Unprocessable Content: Phone Number Format",
            detail="Phone number must be in international number format.",
        )
    return phone_number
