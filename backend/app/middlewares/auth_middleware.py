from functools import wraps
from flask import request, g
from app.utils.error_handler import APIError, raise_api_error
from app.utils.pyjwt import jwt_verifier

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            raise APIError(
                    status=401,
                    title="Unauthorized: Header",
                    detail="Authorization Header does not exist", 
                    pointer="middlewares > auth_middleware.py")
        try:
            token = authorization_header.split(' ')[1]

            if token is None:
                raise APIError(
                        status=401,
                        title="Unauthorized: Token",
                        detail="Token does not exist", 
                        pointer="middlewares > auth_middleware.py")
            
            # tokens to only contain id, email, username
            token_data = jwt_verifier(token)

            # store along request chain
            g.user = token_data
        
        except Exception as err:
            print(err)
            raise_api_error(err, pointer="middlewares > auth_middleware.py")

        # because it is not dependent on anything in try/except block, so can put outside.
        # function will not run unless authorized
        return f(*args, **kwargs)
    
    return decorated_function