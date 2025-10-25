# src/api.py
from flask import Flask
# Importa el Blueprint del controlador para poder registrar sus rutas
from src.controllers.turno_controller import turno_bp

def create_app():
    """
    Función de fábrica para crear la aplicación Flask.
    """
    app = Flask(__name__)
    
    # Registra el Blueprint con todas las rutas de turnos
    app.register_blueprint(turno_bp)
    
    return app
