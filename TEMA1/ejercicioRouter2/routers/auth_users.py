from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#permitirá la autenticación por detrás
oauth2 = OAuth2PasswordBearer(tokenUrl= "login")

#definimos el algoritmo de encriptado
ALGORITHM = "HS256"
#duración del token
ACCESS_TOKEN_EXPIRE_MINUTES = 5
#clave que se utilizará como semilla para generar el token
#comando para ejecutar en git bash (terminal) para que genere un token: openssl rand -hex 32
SECRET_KEY = "dc019e5fcac1b08a8b94bf796c9b004e6128198e434a2eb530efe48436dc83d5"
#objeto que se utilizará para el cálculo hash y de la verificación de la contraseña
password_hash = PasswordHash.recommended()

#router
router = APIRouter()

#clase usuario que hereda de la calse BaseModel que contiene los atributos y los
#datos de un usuario
class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

#se hace esto para que cuando se quiera obtener toda la informacion de un usuario
#no se muestre tambien la contraseña
#clase que hereda de user y solo almacena la contraseña del usuario
class UserDB(User):
    contraseña: str

users_db = {
    "elenarg" : {
        "username" : "elenarg",
        "fullname" : "Elena Rivero",
        "email" : "elenarg@gmail.es",
        "disabled" : False,
        "contraseña" : "Holaholita"
    },
    "prueba" : {
        "username" : "prueba",
        "fullname" : "Prueba Prueba",
        "email" : "prueba@gmail.es",
        "disabled" : False,
        "contraseña" : "Pruebita"
    }
}

@router.post("/register", status_code=201)
def register(usuario: UserDB):

    if usuario.username not in users_db:
        hashed_password = password_hash.hash(usuario.contraseña)
        usuario.contraseña = hashed_password
        users_db[usuario.username] = usuario
        return usuario
    raise HTTPException(status_code=409, detail="El usuario ya existe")