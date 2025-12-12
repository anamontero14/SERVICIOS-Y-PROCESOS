from typing import Optional
from pydantic import BaseModel

#entidad user para la autenticacion
class Cliente(BaseModel):
    username: Optional[str] = None #mirar
    fullname: str
    email: str
    disabled: bool
    password: str #mirar