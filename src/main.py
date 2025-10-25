# src/main.py
from src.api import create_app

# Crea la aplicación Flask llamando a la función de fábrica
app = create_app()

if __name__ == '__main__':
    # Ejecuta la aplicación
    app.run(debug=True, port=5000)
