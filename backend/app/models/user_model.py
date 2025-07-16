import psycopg2.extensions
from app.utils.error_handler import APIError

def create_user(connection: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor, data: dict) -> dict:
    try: 
        # data = {"username": username, "email": email, "password": password}
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s);", (data.get("username"), data.get("email"), data.get("password")))
        connection.commit() # save changes

        # find the last insertion
        cursor.execute("SELECT id, username, email FROM users WHERE username = %s;", (data.get("username"),))
        return cursor.fetchone()
    except Exception as err:
        raise APIError(
            status=500,
            title="Internal Server Error: Database",
            detail=str(err), 
            pointer="user_models.py")

def show_user_via_username_or_email(cursor: psycopg2.extensions.cursor, username: str | None, email: str | None, password_return = False)-> dict | None:
    if not password_return:
        cursor.execute("SELECT id, username, email FROM users WHERE username = %s OR email =%s;", (username, email))
    else:
        cursor.execute("SELECT id, username, email, password FROM users WHERE username = %s OR email =%s;", (username, email))
    return cursor.fetchone()

def show_user(cursor: psycopg2.extensions.cursor, username: str, basic_return=True) -> dict | None:
    if basic_return:
        cursor.execute("SELECT id, username, profile_photo, created_at FROM users WHERE username = %s;", (username, ))
    else:
        cursor.execute("SELECT id, username, email, first_name, last_name, gender, birthday, phone_number, profile_photo, default_shipping_address, created_at, updated_at FROM users WHERE username = %s;", (username, ))
    return cursor.fetchone()

def index_users(cursor: psycopg2.extensions.cursor)-> list[dict]:
    cursor.execute("SELECT id, username, profile_photo, created_at FROM users;")
    return cursor.fetchall()


# @app.route('/bcrypt-sign-up', methods=['POST'])
# def sign_up():
#     # cannot do .values() because order may not be correct
#     username = request.get_json().get('username')
#     password = request.get_json().get('password')

#     if not username or not password:
#         return {"error": "Username & Password required"}, 401

#     try: 
#         connection = get_db_connection()
#         cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

#         # check username exists
#         cursor.execute("SELECT * FROM users WHERE username = %s;", (username, ))
#         existing_user = cursor.fetchone()
#         if existing_user:
#             return {"error": "Username already taken"}, 401
#             # close in finally
        
#         # start hashing password
#         hashed_password = hash_password(password)
#         cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
#         connection.commit() # save changes

#         # find the last insertion
#         cursor.execute("SELECT id, username FROM users WHERE username = %s;", (username,))
#         new_user = cursor.fetchone()

#         return jsonify({"message": "Sign up route reached.", "data":  new_user}), 201
#     except Exception as err:
#         connection.rollback()
#         print(err)
#         return {"error": str(err)}, 401
#     finally:
#         cursor.close()
#         connection.close()