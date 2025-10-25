# src/models/turno_model.py
from dataclasses import dataclass

@dataclass
class Turno:
    """Clase para representar la entidad Turno de la base de datos."""
    id_turno: int
    usuario: str
    cancha: str
    fecha: str
    horario: str
    estado: str
    monto: float # Usamos float para manejar montos con decimales

    def to_dict(self):
        """Convierte la instancia de Turno a un diccionario de Python."""
        return {
            'id_turno': self.id_turno,
            'usuario': self.usuario,
            'cancha': self.cancha,
            'fecha': self.fecha,
            'horario': self.horario,
            'estado': self.estado,
            'monto': self.monto
        }