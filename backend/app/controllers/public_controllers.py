import psycopg2
from app.db.db_connection import get_db_connection
from app.models.user_model import create_user, show_user_via_username_or_email, show_basic_user, index_users

from app.utils.input_validator import username_validator, email_validator, password_validator
from app.utils.error_handler import APIError, raise_api_error
from app.utils.pyjwt import jwt_encoder
from app.utils.bcrypt import hash_password, is_valid_hashed_pw

def sign_up_controller(data: dict) -> dict:
    # check data values
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword').strip()

    # check required values
    if not username or not password or not email:
        raise APIError(
            status=400,
            title="Bad Request: Username, Email, or Password",
            detail="Username, Email, or Password not given", 
            pointer="public_controller.py > sign_up_controller")
    
    # check validation
    username = username_validator(username)
    email = email_validator(email)
    password = password_validator(password)
    # >> check password matches confirmPassword
    if password != confirm_password:
        raise APIError(
            status=400,
            title="Bad Request: Password",
            detail="Passwords given do not match", 
            pointer="public_controller.py > sign_up_controller")

    # compile data
    user_creation_data = {"username": username, "email": email}
    
    # connect to database
    try: 
        (connection, cursor) = get_db_connection()
        
        # check username or email exists
        existing_user = show_user_via_username_or_email(cursor, username=username, email=email)
        if existing_user:
            field, value = (("Username", username) if existing_user.get("username") == username else ("Email", email))
            raise APIError(
                status=409,
                title="Conflict: Username or Email",
                detail=f"{field} `{value}` already exists", 
                pointer="public_controller.py > sign_up_controller")
        

        # start hashing password
        hashed_password = hash_password(password)

        # create user
        user_creation_data["password"] = hashed_password
        new_user = create_user(cursor, user_creation_data)
        connection.commit() # save changes for other connections

        # token generation
        return jwt_encoder(new_user)
    
    except Exception as err:
        connection.rollback()
        raise_api_error(err, pointer="public_controller.py")
    finally:
        cursor.close()
        connection.close()

def sign_in_controller(data: dict)-> dict:
    # check data values
    username_or_email = data.get('usernameOrEmail')
    password = data.get('password')

    if not username_or_email or not password:
        raise APIError(
            status=400,
            title="Bad Request: Username, Email, or Password",
            detail="Username, Email, or Password not given", 
            pointer="public_controller.py > sign_in_controller")

    try:
        # check existing user
        (connection, cursor) = get_db_connection()
        existing_user = show_user_via_username_or_email(cursor, username=username_or_email, email=username_or_email, password_return=True)
        if not existing_user:
            raise APIError(
                status=400,
                title="Bad Request: Login Failed",
                detail="User does not exist", 
                pointer="public_controller.py > sign_in_controller")

        # check password
        if not is_valid_hashed_pw(password, existing_user.get("password")):
            raise APIError(
                status=401,
                title="Unauthorized: Login Failed",
                detail="Incorrect Password", 
                pointer="public_controller.py > sign_in_controller")
        
        # token generation
        return jwt_encoder(existing_user)
    
    except Exception as err:
        connection.rollback()
        raise_api_error(err, pointer="public_controller.py")
    finally:
        cursor.close()
        connection.close()

def show_basic_user_controller(username):
    try: 
        (connection, cursor) = get_db_connection()
        user = show_basic_user(cursor, str(username))
        return user
    except Exception as err:
        raise_api_error(err, pointer="public_controller.py")
    finally:
        cursor.close()
        connection.close()

def index_users_controller()-> list[dict]:
    try: 
        (connection, cursor) = get_db_connection()
        user_list = index_users(cursor)
        return user_list
    except Exception as err:
        raise_api_error(err, pointer="public_controller.py")
    finally:
        cursor.close()
        connection.close()