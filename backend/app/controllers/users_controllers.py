from app.db.db_connection import get_db_connection
from app.models.users_model import show_full_user, show_user_via_username_or_email, update_user, update_user_password
from app.utils.error_handler import raise_api_error, APIError
from app.utils.pyjwt import jwt_encoder
from app.utils.input_validator import username_validator, email_validator, name_validator, gender_validator, phone_number_validator, password_validator
from app.utils.bcrypt import is_valid_hashed_pw, hash_password

def show_full_user_controller(user_id: str) -> dict:
    try: 
        (connection, cursor) = get_db_connection()
        user = show_full_user(cursor, str(user_id))
        return user
    except Exception as err:
        raise_api_error(err, pointer="users_controller.py")
    finally:
        cursor.close()
        connection.close()

def update_owner_controller(data: dict, user_id: str) -> tuple[dict, str]:
    # extract values from data
    username = data.get('username')
    email = data.get('email')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    birthday = data.get('birthday')
    gender = data.get('gender')
    phone_number = data.get('phoneNumber')
    profile_photo = data.get('profilePhoto')
    default_shipping_address = data.get('defaultShippingAddress')

    # no need requirement check for Username or email

    # check values validation
    username = username_validator(username) if username else None
    email = email_validator(email)if email else None
    first_name = name_validator(first_name) if first_name else None
    last_name = name_validator(last_name) if last_name else None
    gender = gender_validator(gender) if gender else None
    phone_number = phone_number_validator(phone_number) if phone_number else None

    try:
        (connection, cursor) = get_db_connection()

        # model - check if username or email already exists
        existing_user = show_full_user(cursor, user_id)
        if not existing_user:
            raise APIError(
                status=404,
                title="Not Found: User",
                detail="User does not exist", 
                pointer="users_controller.py > update_owner_controller")
        # >> set username & email if they are null
        username = username or existing_user.get("username")
        email = email or existing_user.get("email")
        print(username, email)
        # >> skip check if username unchanged OR not inputted
        if username != existing_user.get("username"):
            existing_user_via_username = show_user_via_username_or_email(cursor, username=username)
            if existing_user_via_username and existing_user_via_username.get("id") != user_id:
                raise APIError(
                    status=409,
                    title="Conflict: Username",
                    detail=f"Username `{username}` already exists.",
                    pointer="users_controller.py > update_owner_controller"
                )
        # >> skip check if email unchanged OR not inputted
        if email != existing_user.get("email"):
            existing_user_via_email = show_user_via_username_or_email(cursor, email=email)
            if existing_user_via_email and existing_user_via_email.get("id") != user_id:
                raise APIError(
                    status=409,
                    title="Conflict: Email",
                    detail=f"Email `{email}` already exists.",
                    pointer="users_controller.py > update_owner_controller"
                )

        # model - update using userId
        # updated_at - is updated in SQL
        # compile data
        user_update_data = {"username": username, "email": email, "first_name": first_name, "last_name": last_name, "birthday": birthday, "gender": gender, "phone_number": phone_number, "profile_photo":profile_photo , "default_shipping_address":default_shipping_address}
        updated_full_user = update_user(cursor, user_update_data, user_id)
        connection.commit() 

        # give new token
        updated_basic_user = show_user_via_username_or_email(cursor, username=username)

        return (updated_full_user ,jwt_encoder(updated_basic_user))
    except Exception as err:
        raise_api_error(err, pointer="users_controller.py")
    finally:
        cursor.close()
        connection.close()


def update_owner_password_controller(data: dict, user_id: str) -> dict:

    # extract values from data
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')
    confirm_new_password = data.get('confirmNewPassword').strip()

    # need requirement for any password changes
    if not old_password or not new_password or not confirm_new_password:
        raise APIError(
            status=400,
            title="Bad Request: Passwords",
            detail="Passwords not given", 
            pointer="public_controller.py > update_owner_password_controller")

    # check validation
    new_password = password_validator(new_password)
    # >> check password matches confirmPassword
    if new_password != confirm_new_password:
        raise APIError(
            status=400,
            title="Bad Request: New Password",
            detail="New Passwords given do not match", 
            pointer="public_controller.py > update_owner_password_controller")

    try:
        (connection, cursor) = get_db_connection()
        
        # model - get basic user details & password
        existing_user = show_user_via_username_or_email(cursor, user_id=user_id, password_return=True)
        if not existing_user:
            raise APIError(
                status=404,
                title="Not Found: User",
                detail="User does not exist", 
                pointer="users_controller.py > update_owner_password_controller")
        retrieved_password = existing_user.get('password')

        # model - check if old password matches
        if not is_valid_hashed_pw(old_password, retrieved_password):
            raise APIError(
                status=401,
                title="Unauthorized: Old Password",
                detail="Old Password given is incorrect", 
                pointer="public_controller.py > update_owner_password_controller")
        
        # model - check if new password is the same as old password, raise error that there is no point 400
        if is_valid_hashed_pw(new_password, retrieved_password):
            raise APIError(
                status=422,
                title="Unprocessable Content: New Password",
                detail="New Password given same as Old Password", 
                pointer="public_controller.py > update_owner_password_controller")

        # model - update using userId
        # updated_at - is updated in SQL
        # compile data
        hashed_new_password = hash_password(new_password)
        user_update_data = {"password": hashed_new_password}
        updated_full_user = update_user_password(cursor, user_update_data, user_id)
        connection.commit() 
        return updated_full_user
    except Exception as err:
        raise_api_error(err, pointer="users_controller.py")
    finally:
        cursor.close()
        connection.close()