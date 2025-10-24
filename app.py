#Importamos Flask y jsonify para devolver respuestas JSON
from flask import Flask, jsonify, request
#Importamos la función para conectarnos a la base de datos
from conexionBD import get_connection

#Creamos la app de Flask
app = Flask(__name__)


# RUTA: Obtener todos los turnos (Read - GET)

@app.route('/turnos', methods=['GET'])
def obtener_turnos():
    """
    Devuelve todos los registros de la tabla Turnos en formato JSON.
    Se prueba con un GET a: http://127.0.0.1:5000/turnos
    """
    # Conectarse a la base de datos
    conn = get_connection()
    cursor = conn.cursor()

    # Ejecutar la consulta SQL para obtener todos los turnos
    cursor.execute("SELECT * FROM Turnos")
    resultados = cursor.fetchall()  # Devuelve una lista de tuplas

    # Cerrar la conexión
    conn.close()

    # Convertir las tuplas a diccionarios para JSON
    turnos = []
    for r in resultados:
        turnos.append({
            'id_turno': r[0],
            'usuario': r[1],
            'cancha': r[2],
            'fecha': r[3],
            'horario': r[4],
            'estado': r[5],
            'monto': r[6]
        })

    # Devolver la lista de turnos como JSON
    return jsonify(turnos)


# RUTA: Obtener un turno por ID (Read - GET)

@app.route('/turnos/<int:id_turno>', methods=['GET'])
def obtener_turno(id_turno):
    """
    Devuelve un turno específico por su id_turno.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Turnos WHERE id_turno = ?", (id_turno,))
    r = cursor.fetchone()  # Devuelve solo una tupla

    conn.close()

    if r:
        turno = {
            'id_turno': r[0],
            'usuario': r[1],
            'cancha': r[2],
            'fecha': r[3],
            'horario': r[4],
            'estado': r[5],
            'monto': r[6]
        }
        return jsonify(turno)
    else:
        # Si no existe el turno
        return jsonify({'mensaje': 'Turno no encontrado'}), 404


# RUTA: Crear un nuevo turno (Create - POST)

@app.route('/turnos', methods=['POST'])
def crear_turno():
    """
    Crea un nuevo turno en la base de datos.
    Se envían los datos en el body de la petición en formato JSON.
    """
    datos = request.get_json()  # Obtenemos los datos enviados desde Postman

    # Validamos que vengan todos los campos obligatorios
    required_fields = ['usuario', 'cancha', 'fecha', 'horario', 'estado']
    for campo in required_fields:
        if campo not in datos:
            return jsonify({'mensaje': f'Falta el campo {campo}'}), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Insertamos el turno en la base de datos
    cursor.execute(
        "INSERT INTO Turnos (usuario, cancha, fecha, horario, estado, monto) VALUES (?, ?, ?, ?, ?, ?)",
        (
            datos['usuario'],
            datos['cancha'],
            datos['fecha'],
            datos['horario'],
            datos['estado'],
            datos.get('monto')  # monto es opcional
        )
    )
    conn.commit()  # Guardamos los cambios
    conn.close()

    return jsonify({'mensaje': 'Turno creado correctamente'}), 201


# RUTA: Actualizar un turno (Update - PUT)

@app.route('/turnos/<int:id_turno>', methods=['PUT'])
def actualizar_turno(id_turno):
    """
    Actualiza los datos de un turno existente.
    Se envían los datos en el body de la petición en formato JSON.
    """
    datos = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    # Actualizamos los campos que vienen en la petición
    cursor.execute("""
        UPDATE Turnos
        SET usuario = ?, cancha = ?, fecha = ?, horario = ?, estado = ?, monto = ?
        WHERE id_turno = ?
    """, (
        datos.get('usuario'),
        datos.get('cancha'),
        datos.get('fecha'),
        datos.get('horario'),
        datos.get('estado'),
        datos.get('monto'),
        id_turno
    ))
    conn.commit()
    filas_actualizadas = cursor.rowcount  # Cuántas filas fueron modificadas
    conn.close()

    if filas_actualizadas > 0:
        return jsonify({'mensaje': 'Turno actualizado correctamente'})
    else:
        return jsonify({'mensaje': 'Turno no encontrado'}), 404


# RUTA: Eliminar un turno (Delete - DELETE)

@app.route('/turnos/<int:id_turno>', methods=['DELETE'])
def eliminar_turno(id_turno):
    """
    Elimina un turno de la base de datos según su ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Turnos WHERE id_turno = ?", (id_turno,))
    conn.commit()
    filas_eliminadas = cursor.rowcount
    conn.close()

    if filas_eliminadas > 0:
        return jsonify({'mensaje': 'Turno eliminado correctamente'})
    else:
        return jsonify({'mensaje': 'Turno no encontrado'}), 404


# Ejecutar la app

if __name__ == '__main__':
    # debug=True activa la recarga automática y muestra errores detallados
    app.run(debug=True)
