import psycopg2
from app.db.db_connection import get_db_connection
from app.utils.error_handler import APIError, raise_api_error
from app.utils.pyjwt import jwt_encoder
from app.utils.bcrypt import hash_password, is_valid_hashed_pw
from app.models.user_model import create_user, show_user_via_username_or_email, show_user, index_users

def sign_up_controller(data: dict) -> dict:
    # check data values
    username = data.get('username').strip()
    email = data.get('email').strip()
    password = data.get('password').strip()
    if not username or not password or not email:
        raise APIError(
            status=400,
            title="Bad Request: Username, Email, or Password",
            detail="Username, Email, or Password not given", 
            pointer="public_controller.py > sign_up_controller")
    
    user_creation_data = {"username": username, "email": email}

    # connect to database
    try: 
        (connection, cursor) = get_db_connection()
        
        # check username or email exists
        existing_user = show_user_via_username_or_email(cursor, username, email)
        if existing_user:
            field, value = (("Username", username) if existing_user.get("username") == username else ("Email", email))
            raise APIError(
                status=409,
                title="Conflict: Username or Email",
                detail=f"{field} `{value}` already exists", 
                pointer="public_controller.py > sign_up_controller")
        

        # start hashing password & create user
        hashed_password = hash_password(password)
        user_creation_data["password"] = hashed_password
        new_user = create_user(connection, cursor, user_creation_data)
        connection.commit() # save changes for other connections

        # token generation
        token = jwt_encoder(new_user)
        return new_user
    
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
        (connection, cursor) = get_db_connection()
        existing_user = show_user_via_username_or_email(cursor, username=username_or_email, email=username_or_email, password_return=True)
        if not existing_user:
            raise APIError(
                status=400,
                title="Bad Request: Login Failed",
                detail="User does not exist", 
                pointer="public_controller.py > sign_in_controller")

        # check password
        if is_valid_hashed_pw(password, existing_user.get("password")):
            return jwt_encoder(existing_user)
        else: 
            raise APIError(
                status=401,
                title="Unauthorized: Login Failed",
                detail="Incorrect Password", 
                pointer="public_controller.py > sign_in_controller")

    except Exception as err:
        connection.rollback()
        raise_api_error(err, pointer="public_controller.py")
    finally:
        cursor.close()
        connection.close()

def show_user_controller(username):
    try: 
        (connection, cursor) = get_db_connection()
        user = show_user(cursor, str(username))
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