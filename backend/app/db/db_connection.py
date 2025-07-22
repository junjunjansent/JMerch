import psycopg2
import psycopg2.extras

import os
from dotenv import load_dotenv
from app.utils.error_handler import APIError

# DATABASE_URL=postgresql://neondb_owner:@/users?sslmode=require&channel_binding=require
load_dotenv()

def get_db_connection():
    # db_url = os.getenv('DATABASE_URL')
    # connection = psycopg2.connect(db_url)
    host = os.getenv('POSTGRES_HOST')
    user = os.getenv('POSTGRES_USERNAME')
    password = os.getenv('POSTGRES_PASSWORD')

    if not host or not user or not password:
        raise APIError(
            status=500,
            title=f"Internal Server Error: dot_env",
            detail="Unable to get DB details from dot_env", 
            pointer="db > db_connection.py")

    try:
        connection = psycopg2.connect(
            host=host, 
            database='jmerch',
            user=user,
            password=password,
            sslmode="require")
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return (connection, cursor) # better to return tuple to maintain order
    except Exception as err:
        err_name = err.__class__.__name__
        raise APIError(
            status=503,
            title=f"Service Unavailable: {err_name}",
            detail=str(err), 
            pointer="db > db_connection.py")