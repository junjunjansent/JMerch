import bcrypt

def hash_password(password: str)-> str:
    bytes_hashed_pw =  bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return bytes_hashed_pw.decode('utf-8') # transform to string

def is_valid_hashed_pw(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
