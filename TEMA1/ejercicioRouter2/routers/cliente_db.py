from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from routers.auth_users import authentication
from db.models.cliente import Cliente
from db.client import db_client
from db.schemas.cliente import cliente_schema, clientes_schema
from bson import ObjectId

router = APIRouter(prefix="/clientes", tags= ["clientes"])

clientes_list = []

#funcion para encontrar un cliente por id
def buscar_cliente(nombre: str, apellidos: str):
    #la busqueda me devuelve un objeto del tipo de a BBDD. necesitamos
    #convertirlo a un objeto Cliente
    try:
        #si algo va mal en la búsqueda dentro de la BBDD se lanzará una excepción, así que la controlamos
        cliente = cliente_schema(db_client.local.clientes.find_one({"nombre":nombre, "apellidos":apellidos}))
        return Cliente(**cliente)
    except:
        return {"Error": "Cliente no encontrado"}
    
#funcion para encontrar un cliente por id
def buscar_cliente_id(id: str):
    #la busqueda me devuelve un objeto del tipo de a BBDD. necesitamos
    #convertirlo a un objeto Cliente
    try:
        #si algo va mal en la búsqueda dentro de la BBDD se lanzará una excepción, así que la controlamos
        cliente = cliente_schema(db_client.local.clientes.find_one({"_id": ObjectId(id)}))
        return Cliente(**cliente)
    except:
        return {"Error": "Cliente no encontrado"}

#funcion para encontrar el siguiente id
def next_id():
    for cliente in clientes_list:
        #almacena el id máximo actual
        maximo = 0
        #si el id del cliente actual es mayor al máximo almacenado
        if cliente.id > maximo:
            #el máximo será el id del cliente actual
            maximo = cliente.id
    #le suma 1 al id máximo para pasar al siguiente
    return maximo + 1

#método get para devolver todos los clientes
@router.get("/")
async def clientes():
    #el método find() sin parámetros devuelve todos los registros de la BBDD
    return clientes_schema(db_client.local.clientes.find())

#método para devolver un cliente en específico dependiendo de un atributo
@router.get("")
async def cliente_atributo(id: int):
    cliente = buscar_cliente(id)
    if cliente:
        return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

#método para devolver un cliente con un id específico
@router.get("/{id_cliente}", response_model=Cliente)
async def cliente_id(id_cliente: str):
    return buscar_cliente_id(id_cliente)

#método post para añadir un nuevo cliente a la lista
@router.post("/", status_code= 201, response_model=Cliente)
#para que no todo el mundo tenga acceso a la api creamos el auth_users y ahora tenemos que
#indicar que esté autenticado para que pueda hacer el post
async def añadir_cliente(cliente: Cliente):
    
    if type(buscar_cliente(cliente.nombre, cliente.apellidos)) == Cliente:
        raise HTTPException(status_code=409, detail = "El cliente ya existe")
    
    #transformamos el usuario que recibimos a un diccionario
    cliente_dict = cliente.model_dump()
    #se elimina el campo id por si lo han introducido en el JSON por error
    del cliente_dict["id"]
    #añadimos el usuario a nuestra BBDD
    #obtenemos con inserted_id el id que la BBDD ha generado para nuestro usuario
    id = db_client.local.clientes.insert_one(cliente_dict).inserted_id
    #añadimos el campo id a nuestro diccionario. hay que hacerle un cast
    #a string puesto que el id en BBDD se almacena como un objeto, no como un string
    cliente_dict["id"] = str(id)
    
    #la respuesta de nuestro método es el propio usuario añadido de tipo Cliente
    return Cliente(**cliente_dict)

#método put para actualizar los datos de un cliente existente
@router.put("/{id_cliente}", response_model=Cliente)
async def modificar_cliente(id_cliente: str, cliente_nuevo: Cliente):
    #se convierte el usuario a un diccionario
    cliente_dict = cliente_nuevo.model_dump()
    #eliminamos el id en caso de que venga porque no puede cambiar
    del cliente_dict["id"]
    try:
        #buscamos el id en la BBDD y le pasamos el diccionario con los datos
        #a modificar del usuario
        db_client.local.clientes.find_one_and_replace({"_id":ObjectId(id_cliente)}, cliente_dict)
        #buscamos el objeto en BBDD y lo retornamos, así comprobamos que efectivamente
        #se ha modificado
        return buscar_cliente_id(id_cliente)
    except:   
        #si no se encuentra lanzo una excepción
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

#método para eliminar un cliente
@router.delete("/{id_cliente}", response_model=Cliente)
async def eliminar_cliente(id_cliente: str):
    found = db_client.local.clientes.find_one_and_delete({"_id":ObjectId(id_cliente)})
    
    if not found:
        #si no se encuentra el id se elimina de la excepcion
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return Cliente(**cliente_schema(found))