import psycopg2
import os


def get_db_connection():
    db_url = os.getenv('DATABASE_URL')
    # connection = psycopg2.connect(db_url)
    connection = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'), 
        database='JMerch',
        user=os.getenv('POSTGRES_USERNAME'),
        password=os.getenv('POSTGRES_PASSWORD'),
        sslmode="require")
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return (connection, cursor) # better to return tuple to maintain order

# DATABASE_URL=postgresql://neondb_owner:@/users?sslmode=require&channel_binding=require