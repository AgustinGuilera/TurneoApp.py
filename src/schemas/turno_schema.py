# src/schemas/turno_schema.py
from pydantic import BaseModel, Field

class TurnoInputSchema(BaseModel):
    """
    Esquema de validación para la entrada de datos (usado en POST y PUT).
    Asegura que todos los campos requeridos estén presentes y sean válidos.
    """
    usuario: str = Field(min_length=1)
    cancha: str = Field(min_length=1)
    fecha: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$", description="Formato YYYY-MM-DD")
    horario: str = Field(min_length=1)
    estado: str = Field(min_length=1)
    monto: float | None = None # Monto es opcional en la petición

    class Config:
        from_attributes = True

class TurnoResponseSchema(BaseModel):
    """
    Esquema para la salida de datos (usado en GET).
    """
    id_turno: int
    usuario: str
    cancha: str
    fecha: str
    horario: str
    estado: str
    monto: float | None = None