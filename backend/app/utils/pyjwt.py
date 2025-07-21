from dotenv import load_dotenv
import os

load_dotenv()
jwt_secret = os.getenv('JWT_SECRET')
if not jwt_secret:
    raise APIError(
        status=500,
        title="Internal Server Error: JWT Secret",
        detail="JWT Secret is missing", 
        pointer="util > pyjwt.py")

# ---------- token generation functions

import jwt
from app.utils.error_handler import APIError

def jwt_encoder(payload: dict) -> str:
    try: 
        token = jwt.encode(payload, jwt_secret, algorithm="HS256")            
        return token
    except Exception as err:
        err_name = err.__class__.__name__
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="util > pyjwt.py")

def jwt_verifier(token: str) -> dict:
    try: 
        decoded_token = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return decoded_token
    except Exception as err:
        err_name = err.__class__.__name__
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="util > pyjwt.py")
