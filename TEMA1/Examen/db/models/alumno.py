from typing import Optional
from pydantic import BaseModel

#entidad alumno
class Alumno(BaseModel):
    id: Optional[str] = None
    nombre: str
    apellidos: str
    fecha_nacimiento: str
    curso: str
    repetidor: bool
    id_colegio: str