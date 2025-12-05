from datetime import *
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import jwt
from jwt import PyJWTError
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
#objeto que se utilizará para el cálculo hash y de la verificación de la password
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
#no se muestre tambien la password
#clase que hereda de user y solo almacena la password del usuario
class UserDB(User):
    password: str

users_db = {
    "elenarg" : {
        "username" : "elenarg",
        "fullname" : "Elena Rivero",
        "email" : "elenarg@gmail.es",
        "disabled" : False,
        "password" : "$argon2id$v=19$m=65536,t=3,p=4$X4TU7UuYAm4nqLnL/e4Xcw$kE2HUP23oaKstoUE5aAImNKk+Gj7q/n12ntmdsmxDnk"
    },
    "prueba" : {
        "username" : "prueba",
        "fullname" : "Prueba Prueba",
        "email" : "prueba@gmail.es",
        "disabled" : False,
        "password" : "$argon2id$v=19$m=65536,t=3,p=4$LFVGM2D1ydcMsnvpHwje1w$5Rt6EZX3pAM7j3UezXNrA/28kZ3C11K0t0hy2Ni3lEk"
    }
}

@router.post("/register", status_code=201)
def register(usuario: UserDB):

    if usuario.username not in users_db:
        hashed_password = password_hash.hash(usuario.password)
        usuario.password = hashed_password
        users_db[usuario.username] = usuario.model_dump()
        return usuario
    raise HTTPException(status_code=409, detail="El usuario ya existe")

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if user_db:
        try:
            #si el suuario existe en la base de datos
            #comprobamos las passwords
            #obtiene un objeto que devuelve un diccionario con todos los valores del objeto
            #los ** sirven para crear este objeto
            user = UserDB(**user_db)
            if password_hash.verify(form.password, user.password):
                expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                #diccionario con campo que guarda el username y el tiempo de expiracion
                access_token = {"sub": user.username, "exp": expire}
                #generamos el token
                token = jwt.encode(access_token, SECRET_KEY, algorithm= ALGORITHM)
                return {"access_token": token, "token_type" : "bearer"}
        except:
            raise HTTPException(status_code = 400, detail = "Error al verificar contraseña")
    raise HTTPException(status_code = 401, detail = "Usuario o password incorrectos")

#lo que pretende esta funcion es devolvernos al usuario a traves del token
async def authentication(token: str = Depends(oauth2)):
    try:
        #sub porque es el campo en el que almaceno el campo del usuario para ver si existe en
        #la base de datos y si está activo. Estamos decodificando el token para obtener el user
        #nos devuelve un diccionario y nosotros solo queremos el usuario, por lo que hacemos un get del diccionario
        username = jwt.decode(token, SECRET_KEY, algorithm= ALGORITHM).get("sub")
        #nos tenemos que asegurar que el ususario no está vacío, que no está a None
        if username is None:
            #lanzo una excepción
            raise HTTPException(status_code = 401, detail = "Credenciales de autenticación inválidas",
                                #es una información extra donde se puede consultar más datos
                                headers = {"WWW-Authenticate" : "Bearer"})
    except PyJWTError:
        #lanzo una excepción
            raise HTTPException(status_code = 401, detail = "Credenciales de autenticación inválidas",
                                headers = {"WWW-Authenticate" : "Bearer"})
            
    #si todo va bien hasta aquí creamos un user igualado a el username de nuestra bbdd
    user = User(**users_db[username])
    
    #ya que tenemos al usuario y sus datos tenemos que comprobar si está deshabilitado o no
    #comprobamos el booleano que contiene el atributo disabled de la entidad User
    if user.disabled:
        #si está deshabilitado mandamos una excepción
        raise HTTPException(status_code = 400, detail = "Usuario inactivo")
    #si no devolvemos el usuario
    return user