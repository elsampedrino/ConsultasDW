# app/database/teradata_connection.py
import os
from dotenv import load_dotenv
import teradatasql
import json

# Cargar variables desde el archivo .env
load_dotenv()

def get_teradata_connection():
    try:
        conn_dict = {
            "host": os.getenv("TERADATA_HOST"),
            "user": os.getenv("TERADATA_USER"),
            "password": os.getenv("TERADATA_PASSWORD"),
            "logmech": os.getenv("TERADATA_LOGMECH")
        }
    
        conn_str = json.dumps(conn_dict)
        return teradatasql.connect(conn_str)

    except Exception as e:
        raise Exception(f"Error al conectar con SQL Server: {str(e)}")


