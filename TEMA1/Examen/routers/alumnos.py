from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from routers.auth_users import authentication
from db.models.alumno import Alumno
from db.client import db_client
from db.schemas.alumno import alumno_schema, alumnos_schema
from bson import ObjectId

router = APIRouter(prefix="/alumnos", tags= ["alumnos"])

alumnos_list = []

#funcion para encontrar un alumno por id
def buscar_alumno(nombre: str, apellidos: str):
    #la busqueda me devuelve un objeto del tipo de a BBDD. necesitamos
    #convertirlo a un objeto Alumno
    try:
        #si algo va mal en la búsqueda dentro de la BBDD se lanzará una excepción, así que la controlamos
        alumno = alumno_schema(db_client.local.alumnos.find_one({"nombre":nombre, "apellidos":apellidos}))
        return Alumno(**alumno)
    except:
        return {"Error": "Alumno no encontrado"}
    
#funcion para encontrar un alumno por id
def buscar_alumno_id(id: str):
    #la busqueda me devuelve un objeto del tipo de a BBDD. necesitamos
    #convertirlo a un objeto Alumno
    try:
        #si algo va mal en la búsqueda dentro de la BBDD se lanzará una excepción, así que la controlamos
        alumno = alumno_schema(db_client.local.alumnos.find_one({"_id": ObjectId(id)}))
        return Alumno(**alumno)
    except:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
#funcion para encontrar un alumno por curso
def buscar_alumno_curso(curso: str):
    #la busqueda me devuelve un objeto del tipo de a BBDD. necesitamos
    #convertirlo a un objeto Alumno
    try:
        #si algo va mal en la búsqueda dentro de la BBDD se lanzará una excepción, así que la controlamos
        alumno = alumno_schema(db_client.local.alumnos.find_one({"curso": curso}))
        return Alumno(**alumno)
    except:
        return {"Error": "Alumno no encontrado"}

#funcion para encontrar el siguiente id
def next_id():
    for alumno in alumnos_list:
        #almacena el id máximo actual
        maximo = 0
        #si el id del alumno actual es mayor al máximo almacenado
        if alumno.id > maximo:
            #el máximo será el id del alumno actual
            maximo = alumno.id
    #le suma 1 al id máximo para pasar al siguiente
    return maximo + 1

#método get para devolver todos los alumnos
@router.get("/")
async def alumnos():
    #el método find() sin parámetros devuelve todos los registros de la BBDD
    return alumnos_schema(db_client.local.alumnos.find())

#método para devolver un alumno en específico dependiendo de un atributo
@router.get("", response_model=Alumno)
async def alumno(curso: str):
    return buscar_alumno_curso(curso)

#método para devolver un alumno con un id específico
@router.get("/{id_alumno}", response_model=Alumno)
async def alumno_id(id_alumno: str):
    return buscar_alumno_id(id_alumno)

#método post para añadir un nuevo alumno a la lista
@router.post("/", status_code= 201, response_model=Alumno)
#para que no todo el mundo tenga acceso a la api creamos el auth_users y ahora tenemos que
#indicar que esté autenticado para que pueda hacer el post
async def añadir_alumno(alumno: Alumno):
    #comprueba que el alumno ya exista
    if type(buscar_alumno(alumno.nombre, alumno.apellidos)) == Alumno:
        raise HTTPException(status_code=409, detail = "El alumno ya existe")
    
    #transformamos el usuario que recibimos a un diccionario
    alumno_dict = alumno.model_dump()
    
    #se elimina el campo id por si lo han introducido en el JSON por error
    del alumno_dict["id"]
    #añadimos el usuario a nuestra BBDD
    #obtenemos con inserted_id el id que la BBDD ha generado para nuestro usuario
    id = db_client.local.alumnos.insert_one(alumno_dict).inserted_id
    
    #if (db_client.local.colegios.find_one({"_id"}))
    #añadimos el campo id a nuestro diccionario. hay que hacerle un cast
    #a string puesto que el id en BBDD se almacena como un objeto, no como un string
    alumno_dict["id"] = str(id)
    
    #la respuesta de nuestro método es el propio usuario añadido de tipo Alumno
    return Alumno(**alumno_dict)

#método put para actualizar los datos de un alumno existente
@router.put("/{id_alumno}", response_model=Alumno, status_code=200)
async def modificar_alumno(id_alumno: str, alumno_nuevo: Alumno):
    #se convierte el usuario a un diccionario
    alumno_dict = alumno_nuevo.model_dump()
    #eliminamos el id en caso de que venga porque no puede cambiar
    del alumno_dict["id"]
    try:
        #buscamos el id en la BBDD y le pasamos el diccionario con los datos
        #a modificar del usuario
        db_client.local.alumnos.find_one_and_replace({"_id":ObjectId(id_alumno)}, alumno_dict)
        #buscamos el objeto en BBDD y lo retornamos, así comprobamos que efectivamente
        #se ha modificado
        return buscar_alumno_id(id_alumno)
    except:   
        #si no se encuentra lanzo una excepción
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

#método para eliminar un alumno
@router.delete("/{id_alumno}", response_model=Alumno)
async def eliminar_alumno(id_alumno: str):
    
    found = buscar_alumno_id(id_alumno)
    
    if not found:
        #si no se encuentra el id se elimina de la excepcion
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return Alumno(**alumno_schema(found))