from typing import Optional
from pydantic import BaseModel

#entidad user
class Cliente(BaseModel):
    id: Optional[str] = None
    nombre: str
    apellidos: str
    telefono: int
    email: str