# src/database/connection.py
import pyodbc
from typing import Any

# Configuraciones de conexión
CONNECTION_STRING = (
    'DRIVER={SQL Server};'
    'SERVER=HP-Mateo;'
    'DATABASE=Turnero BD;'
    'Trusted_Connection=yes;'
)

def get_connection() -> pyodbc.Connection:
    """
    Función que crea y devuelve una conexión a la base de datos SQL Server.
    """
    try:
        connection = pyodbc.connect(CONNECTION_STRING)
        return connection
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Error de conexión a la base de datos: {sqlstate}")
        raise
