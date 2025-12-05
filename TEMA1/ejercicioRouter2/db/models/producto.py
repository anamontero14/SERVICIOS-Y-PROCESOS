from typing import Optional
from pydantic import BaseModel

class Producto(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: str
    precio: float
    idCliente: int