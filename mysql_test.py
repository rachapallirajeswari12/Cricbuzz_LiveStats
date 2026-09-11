import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "cricbuzz_livestats")
    )

    if conn.is_connected():
        print("MySQL connection successful!")
        print("Database:", conn.database)

    conn.close()

except mysql.connector.Error as err:
    print("MySQL connection failed:", err)