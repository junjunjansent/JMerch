import psycopg2.extensions
from app.utils.error_handler import APIError

def show_cart(cursor: psycopg2.extensions.cursor, user_id: str ) -> dict :
    return

def create_cart(cursor: psycopg2.extensions.cursor, data: dict, user_id: str ) -> dict :
    return

def update_cart(cursor: psycopg2.extensions.cursor, data: dict, user_id: str ) -> dict :
    return

def destroy_cart(cursor: psycopg2.extensions.cursor, user_id: str ) -> dict :
    return