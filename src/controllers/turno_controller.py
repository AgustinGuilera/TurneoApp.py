# src/controllers/turno_controller.py
from flask import Blueprint, jsonify, request
from src.services.turno_service import TurnoService
from src.schemas.turno_schema import TurnoInputSchema, TurnoResponseSchema 
from pydantic import ValidationError

# Define el Blueprint (sub-aplicación) con el prefijo /turnos
turno_bp = Blueprint('turno_bp', __name__, url_prefix='/turnos')
turno_service = TurnoService()

@turno_bp.route('', methods=['GET'])
def get_all_turnos():
    """
    RUTA: Devuelve una lista con todos los turnos. (GET /turnos)
    """
    turnos_list = turno_service.get_all_turnos()
    
    # Mapeamos la lista de objetos Turno a una lista de diccionarios JSON
    # Usamos .to_dict() para que Pydantic pueda validar correctamente el objeto Turno
    response_data = [TurnoResponseSchema.model_validate(t.to_dict()).model_dump() for t in turnos_list]
    
    return jsonify(response_data), 200


@turno_bp.route('/<int:id_turno>', methods=['GET'])
def get_turno(id_turno):
    """
    RUTA: Devuelve un turno específico por su id_turno. (GET /turnos/1)
    """
    turno_obj = turno_service.get_turno_by_id(id_turno)

    if turno_obj:
        # Usamos .to_dict() para la validación y serialización
        response_data = TurnoResponseSchema.model_validate(turno_obj.to_dict()).model_dump()
        return jsonify(response_data), 200
    else:
        return jsonify({'mensaje': 'Turno no encontrado'}), 404


@turno_bp.route('', methods=['POST'])
def crear_turno():
    """
    RUTA: Crea un nuevo turno.
    """
    try:
        # Asegura que Flask procese el cuerpo de la petición como JSON
        datos_json = request.get_json(force=True)
        # Valida los datos entrantes con el esquema Pydantic
        datos = TurnoInputSchema.model_validate(datos_json)
        
        if turno_service.create_turno(datos):
            return jsonify({'mensaje': 'Turno creado correctamente'}), 201
        else:
            return jsonify({'mensaje': 'Error interno al crear el turno'}), 500

    except ValidationError as e:
        return jsonify({'mensaje': 'Error de validación de datos', 'errores': e.errors()}), 400
    except Exception as e:
        print(f"Error en la petición POST: {e}") 
        return jsonify({'mensaje': 'Error en la petición. Revisa el formato JSON.'}), 400


@turno_bp.route('/<int:id_turno>', methods=['PUT'])
def actualizar_turno(id_turno):
    """
    RUTA: Actualiza un turno existente.
    """
    try:
        datos_json = request.get_json(force=True)
        datos = TurnoInputSchema.model_validate(datos_json)

        if turno_service.update_turno(id_turno, datos):
            return jsonify({'mensaje': 'Turno actualizado correctamente'}), 200
        else:
            return jsonify({'mensaje': 'Turno no encontrado o no se pudo actualizar'}), 404

    except ValidationError as e:
        return jsonify({'mensaje': 'Error de validación de datos', 'errores': e.errors()}), 400
    except Exception as e:
        print(f"Error en la petición PUT: {e}")
        return jsonify({'mensaje': 'Error en la petición. Revisa el formato JSON.'}), 400


@turno_bp.route('/<int:id_turno>', methods=['DELETE'])
def eliminar_turno(id_turno):
    """
    RUTA: Elimina un turno.
    """
    if turno_service.delete_turno(id_turno):
        return jsonify({'mensaje': 'Turno eliminado correctamente'}), 200
    else:
        return jsonify({'mensaje': 'Turno no encontrado'}), 404