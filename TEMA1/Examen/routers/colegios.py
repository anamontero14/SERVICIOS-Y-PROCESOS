from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from routers.auth_users import authentication
from db.models.colegio import Colegio
from db.models.alumno import Alumno
from db.client import db_client
from db.schemas.colegio import colegio_schema, colegios_schema
from db.schemas.alumno import alumno_schema, alumnos_schema
from bson import ObjectId

router = APIRouter(prefix="/colegios", tags= ["colegios"])

colegios_list = []

#funcion para encontrar un colegio por id
def buscar_colegio(nombre: str, distrito: str):
    #la busqueda me devuelve un objeto del tipo de a BBDD. necesitamos
    #convertirlo a un objeto Colegio
    try:
        #si algo va mal en la búsqueda dentro de la BBDD se lanzará una excepción, así que la controlamos
        colegio = colegio_schema(db_client.local.colegios.find_one({"nombre":nombre, "distrito":distrito}))
        return Colegio(**colegio)
    except:
        return {"Error": "Colegio no encontrado"}
    
#funcion para encontrar un colegio por id
def buscar_colegio_id(id: str):
    #la busqueda me devuelve un objeto del tipo de a BBDD. necesitamos
    #convertirlo a un objeto Colegio
    try:
        #si algo va mal en la búsqueda dentro de la BBDD se lanzará una excepción, así que la controlamos
        colegio = colegio_schema(db_client.local.colegios.find_one({"_id": ObjectId(id)}))
        return Colegio(**colegio)
    except:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")

#funcion para encontrar el siguiente id
def next_id():
    for colegio in colegios_list:
        #almacena el id máximo actual
        maximo = 0
        #si el id del colegio actual es mayor al máximo almacenado
        if colegio.id > maximo:
            #el máximo será el id del colegio actual
            maximo = colegio.id
    #le suma 1 al id máximo para pasar al siguiente
    return maximo + 1

def buscar_alumno(id_colegio: str):
    try:
        alumno = alumnos_schema(db_client.local.alumnos.find({"id_colegio": id_colegio}))
        return Alumno(**alumno)
    except:
        return {"Error" : "El colegio no se ha encontrado"}

#método get para devolver todos los colegios
@router.get("/")
async def colegios():
    #el método find() sin parámetros devuelve todos los registros de la BBDD
    return colegios_schema(db_client.local.colegios.find())

#método para devolver un colegio con un id específico
@router.get("/{id_colegio}", response_model=Colegio)
async def colegio_id(id_colegio: str):
    found = buscar_colegio_id(id_colegio)
    
    if not found:
        #si no se encuentra el id se elimina de la excepcion
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    return buscar_colegio_id(id_colegio)

#método para devolver un colegio con un id específico
@router.get("/{id_colegio}/alumnos", response_model=Colegio)
async def colegios_alumnos(id_colegio: str):
    colegios = buscar_colegio_id(id_colegio)
    
    if colegios:
        alumnos = buscar_alumno(id_colegio)
        if alumnos:
            return alumnos
        raise HTTPException(status_code=404, detail="No hay alumnos encontrados para el colegio")
    raise HTTPException(status_code=404, detail="Colegio no encontrado")

#método post para añadir un nuevo colegio a la lista
@router.post("/", status_code= 201, response_model=Colegio)
async def añadir_colegio(colegio: Colegio):
    #comprueba que el colegio ya exista
    if type(buscar_colegio(colegio.nombre, colegio.distrito)) == Colegio:
        raise HTTPException(status_code=409, detail = "El colegio ya existe")
    
    #transformamos el usuario que recibimos a un diccionario
    colegio_dict = colegio.model_dump() 
    
    #comprueba que el colegio tiene un tipo apropiado
    if (colegio.tipo != "publico" and colegio.tipo != "concertado" and colegio.tipo != "privado"):
        #Bajo mi punto de vista devolvería un código 400 porque el usuario es el que ha formado
        #mal la petición, no considero que sea ningún problema del servidor
        raise HTTPException(status_code=400, detail = "El colegio no se pudo crear")
    else: 
        #se elimina el campo id por si lo han introducido en el JSON por error
        del colegio_dict["id"]
        #añadimos el usuario a nuestra BBDD
        #obtenemos con inserted_id el id que la BBDD ha generado para nuestro usuario
        id = db_client.local.colegios.insert_one(colegio_dict).inserted_id
        #añadimos el campo id a nuestro diccionario. hay que hacerle un cast
        #a string puesto que el id en BBDD se almacena como un objeto, no como un string
        colegio_dict["id"] = str(id)
        
        #la respuesta de nuestro método es el propio usuario añadido de tipo Colegio
        return Colegio(**colegio_dict)

#método para eliminar un colegio
@router.delete("/{id_colegio}", response_model=Colegio)
async def eliminar_colegio(id_colegio: str):
    found = db_client.local.colegios.find_one_and_delete({"_id":ObjectId(id_colegio)})
    
    if not found:
        #si no se encuentra el id se elimina de la excepcion
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    return Colegio(**colegio_schema(found))