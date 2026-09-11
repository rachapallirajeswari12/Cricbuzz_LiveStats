import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    # Streamlit Cloud: read database details from Streamlit Secrets
    try:
        import streamlit as st

        if "mysql" in st.secrets:
            config = st.secrets["mysql"]

            return mysql.connector.connect(
                host=config["host"],
                port=int(config["port"]),
                user=config["user"],
                password=config["password"],
                database=config["database"],
                ssl_disabled=False,
            )
    except Exception:
        pass

    # Local computer: read database details from .env
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "cricbuzz_livestats"),
    )