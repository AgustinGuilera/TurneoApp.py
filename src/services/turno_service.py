# src/services/turno_service.py
from src.database.connection import get_connection
from src.models.turno_model import Turno
from src.schemas.turno_schema import TurnoInputSchema
import pyodbc
from typing import List, Optional # Importamos List para la nueva función

class TurnoService:
    """
    Contiene la lógica de negocio y la interacción directa con la base de datos (CRUD).
    """

    @staticmethod
    def _map_row_to_turno(row: tuple) -> Turno:
        """
        Función auxiliar para mapear una tupla de la DB a un objeto Turno.
        """
        # (id_turno, usuario, cancha, fecha, horario, estado, monto)
        return Turno(
            id_turno=row[0],
            usuario=row[1],
            cancha=row[2],
            fecha=row[3],
            horario=row[4],
            estado=row[5],
            monto=row[6]
        )
    
    # -------------------------------------------------------------
    # NUEVA FUNCIÓN: Obtener todos los turnos
    # -------------------------------------------------------------
    def get_all_turnos(self) -> List[Turno]:
        """Devuelve una lista con todos los turnos de la tabla."""
        conn = get_connection()
        cursor = conn.cursor()
        turnos = []

        try:
            cursor.execute("SELECT * FROM Turnos") # Consulta para traer todo
            for row in cursor.fetchall():
                turnos.append(self._map_row_to_turno(row))
            return turnos
        except pyodbc.Error as ex:
            print(f"Error al obtener todos los turnos: {ex}")
            # Si hay un error, devolvemos una lista vacía para evitar un crash
            return [] 
        finally:
            conn.close()

    def get_turno_by_id(self, id_turno: int) -> Optional[Turno]:
        """Devuelve un turno específico por su id_turno."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM Turnos WHERE id_turno = ?", (id_turno,))
            row = cursor.fetchone()
            return self._map_row_to_turno(row) if row else None
        finally:
            conn.close()

    def create_turno(self, datos: TurnoInputSchema) -> bool:
        """Crea un nuevo turno en la base de datos."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Los datos ya están validados por Pydantic
            cursor.execute(
                "INSERT INTO Turnos (usuario, cancha, fecha, horario, estado, monto) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    datos.usuario,
                    datos.cancha,
                    datos.fecha,
                    datos.horario,
                    datos.estado,
                    datos.monto
                )
            )
            conn.commit()
            return True
        except pyodbc.Error as ex:
            print(f"Error al crear turno: {ex}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def update_turno(self, id_turno: int, datos: TurnoInputSchema) -> bool:
        """Actualiza los datos de un turno existente."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE Turnos
                SET usuario = ?, cancha = ?, fecha = ?, horario = ?, estado = ?, monto = ?
                WHERE id_turno = ?
            """, (
                datos.usuario,
                datos.cancha,
                datos.fecha,
                datos.horario,
                datos.estado,
                datos.monto,
                id_turno
            ))
            conn.commit()
            return cursor.rowcount > 0 
        except pyodbc.Error as ex:
            print(f"Error al actualizar turno: {ex}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def delete_turno(self, id_turno: int) -> bool:
        """Elimina un turno de la base de datos."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM Turnos WHERE id_turno = ?", (id_turno,))
            conn.commit()
            return cursor.rowcount > 0 
        except pyodbc.Error as ex:
            print(f"Error al eliminar turno: {ex}")
            conn.rollback()
            return False
        finally:
            conn.close()