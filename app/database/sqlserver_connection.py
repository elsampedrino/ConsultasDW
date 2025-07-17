import pyodbc
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_sqlserver_connection():
    try:
        server = os.getenv("SQLSERVER_HOST")
        database = os.getenv("SQLSERVER_DATABASE")
        username = os.getenv("SQLSERVER_USER")
        password = os.getenv("SQLSERVER_PASSWORD")

        if not all([server, database, username, password]):
            raise Exception("Faltan parámetros de conexión en el archivo .env")

        # Cadena de conexión usando SQL Authentication
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
        )

        conn = pyodbc.connect(connection_string)
        return conn

    except Exception as e:
        raise Exception(f"Error al conectar con SQL Server: {str(e)}")
