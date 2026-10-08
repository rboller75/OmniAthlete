from database import get_connection

try:
    connection = get_connection()

    print("Successfully connected to PostgreSQL!")

    connection.close()
    print("Connection closed.")

except Exception as error:
    print("Database connection failed:")
    print(error)