import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Create and return a PostgreSQL database connection."""
    
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set in the .env file")

    return psycopg.connect(database_url)

from database import get_connection

try:
    connection = get_connection()
    print("Successfully connected to PostgreSQL!")

    connection.close()
    print("Connection closed.")

except Exception as error:
    print("Database connection failed:")
    print(error)