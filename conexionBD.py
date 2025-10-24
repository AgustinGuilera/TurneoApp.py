# Este archivo se encarga de manejar la conexión con la base de datos SQL Server

import pyodbc  # Librería para conectarse a SQL Server desde Python

def get_connection():
    """ Función que crea y devuelve una conexión a la base de datos SQL Server. """

    connection = pyodbc.connect(
        'DRIVER={SQL Server};'          # Tipo de base de datos (SQL Server)
        'SERVER=HP-Mateo;'             # Nombre del servidor
        'DATABASE=Turnero BD;'       # Nombre de la base de datos 
        'Trusted_Connection=yes;'       # Si usás autenticación de Windows;
    )
    return connection  # Devuelve la conexión activa
