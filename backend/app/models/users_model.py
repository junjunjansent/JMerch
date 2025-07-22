import psycopg2.extensions
from app.utils.error_handler import APIError

# Use dict["key"] here because we dont want to search for None value if obtained via .get("key")

def create_user(cursor: psycopg2.extensions.cursor, data: dict) -> dict:
    try: 
        # data = {"username": username, "email": email, "password": password}
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s);", (data["username"], data["email"], data["password"]))

        # find the last insertion
        cursor.execute("SELECT id, username, email FROM users WHERE username = %s;", (data["username"],))
        return cursor.fetchone()
    except Exception as err:
        raise APIError(
            status=500,
            title="Internal Server Error: Database",
            detail=str(err), 
            pointer="users_model.py > create_user")

# main function to get token
def show_user_via_username_or_email(
    cursor: psycopg2.extensions.cursor, 
    username: str | None = None, 
    email: str | None = None, 
    password_return = False, 
    user_id: str = None
)-> dict | None:
    if not (username or email or user_id):
        raise APIError(
            status=501,
            title="Not Implemented: Database",
            detail="No Username, Email, Id given to search User Table", 
            pointer="users_model.py > show_user_via_username_or_email")
    elif not password_return:
        cursor.execute("SELECT id, username, email FROM users WHERE username = %s OR email =%s;", (username, email))
    elif password_return and user_id:
        cursor.execute("SELECT id, username, email, password FROM users WHERE id = %s;", (user_id, ))
    else:
        cursor.execute("SELECT id, username, email, password FROM users WHERE username = %s OR email =%s;", (username, email))
    return cursor.fetchone()

def show_basic_user(cursor: psycopg2.extensions.cursor, username: str) -> dict | None:
    cursor.execute("SELECT id, username, created_at FROM users WHERE username = %s;", (username, ))
    return cursor.fetchone()

def show_full_user(cursor: psycopg2.extensions.cursor, user_id: str) -> dict | None:
    cursor.execute("""SELECT 
                        id, username, email, 
                        first_name, last_name, 
                        gender, birthday, phone_number, 
                        profile_photo, default_shipping_address, 
                        created_at, updated_at 
                   FROM users 
                   WHERE id = %s;""", 
                   (user_id, ))
    return cursor.fetchone()

def index_users(cursor: psycopg2.extensions.cursor)-> list[dict]:
    cursor.execute("SELECT id, username, profile_photo, created_at FROM users;")
    return cursor.fetchall()

def update_user(cursor: psycopg2.extensions.cursor, data: dict, user_id: str) -> dict:
    try: 
        cursor.execute("""UPDATE users SET 
                            username = %s, email = %s,
                            first_name = %s, last_name = %s, 
                            birthday = %s, gender = %s, 
                            phone_number = %s, profile_photo = %s, 
                            default_shipping_address = %s, 
                            updated_at = CURRENT_TIMESTAMP 
                       WHERE id = %s""", (
                           data["username"], data["email"], 
                           data["first_name"], data["last_name"], 
                           data["birthday"], data["gender"], 
                           data["phone_number"], data["profile_photo"], 
                           data["default_shipping_address"], 
                           user_id))

        # find the last insertion
        cursor.execute("""SELECT 
                       id, username, email, 
                            first_name, last_name, 
                            gender, birthday, phone_number,
                            profile_photo, default_shipping_address, 
                            created_at, updated_at 
                       FROM users WHERE id = %s;""", 
                       (user_id, ))
        return cursor.fetchone()
    except Exception as err:
        raise APIError(
            status=500,
            title="Internal Server Error: Database",
            detail=str(err), 
            pointer="users_model.py > update_user")

def update_user_password(cursor: psycopg2.extensions.cursor, data: dict, user_id: str) -> dict:
    try:
        cursor.execute("""
                       UPDATE users SET 
                            password = %s, 
                            updated_at = CURRENT_TIMESTAMP 
                       WHERE id = %s;""", (data["password"], user_id))

        # find the last insertion
        cursor.execute("""SELECT 
                            id, username, email, 
                            first_name, last_name, 
                            gender, birthday, phone_number, 
                            profile_photo, default_shipping_address, 
                            created_at, updated_at 
                       FROM users 
                       WHERE id = %s;""", 
                       (user_id, ))
        return cursor.fetchone()
    except Exception as err:
        raise APIError(
            status=500,
            title="Internal Server Error: Database",
            detail=str(err), 
            pointer="users_model.py > update_user_password")