from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db.models.producto import Producto
from db.client import db_client
from db.schemas.producto import producto_schema, productos_schema
from bson import ObjectId

router = APIRouter(prefix="/productos", tags= ["productos"])

productos_list = []

#funcion para encontrar un producto por id
def buscar_producto(nombre: str, descripcion: str):
    #la busqueda me devuelve un objeto del tipo de a BBDD. necesitamos
    #convertirlo a un objeto producto
    try:
        #si algo va mal en la búsqueda dentro de la BBDD se lanzará una excepción, así que la controlamos
        producto = producto_schema(db_client.local.productos.find_one({"nombre":nombre, "descripcion":descripcion}))
        return Producto(**producto)
    except:
        return {"Error": "producto no encontrado"}
    
#funcion para encontrar un producto por id
def buscar_producto_id(id: str):
    #la busqueda me devuelve un objeto del tipo de a BBDD. necesitamos
    #convertirlo a un objeto producto
    try:
        #si algo va mal en la búsqueda dentro de la BBDD se lanzará una excepción, así que la controlamos
        producto = producto_schema(db_client.local.productos.find_one({"_id": ObjectId(id)}))
        return Producto(**producto)
    except:
        return {"Error": "producto no encontrado"}

#funcion para encontrar el siguiente id
def next_id():
    for producto in productos_list:
        #almacena el id máximo actual
        maximo = 0
        #si el id del producto actual es mayor al máximo almacenado
        if producto.id > maximo:
            #el máximo será el id del producto actual
            maximo = producto.id
    #le suma 1 al id máximo para pasar al siguiente
    return maximo + 1

#método get para devolver todos los productos
@router.get("/")
async def productos():
    #el método find() sin parámetros devuelve todos los registros de la BBDD
    return productos_schema(db_client.local.productos.find())

#método para devolver un producto en específico dependiendo de un atributo
@router.get("")
async def producto_atributo(id: int):
    producto = buscar_producto(id)
    if producto:
        return producto
    raise HTTPException(status_code=404, detail="producto no encontrado")

#método para devolver un producto con un id específico
@router.get("/{id_producto}", response_model=Producto)
async def producto_id(id_producto: str):
    return buscar_producto_id(id_producto)

#método post para añadir un nuevo producto a la lista
@router.post("/", status_code= 201, response_model=Producto)
#para que no todo el mundo tenga acceso a la api creamos el auth_users y ahora tenemos que
#indicar que esté autenticado para que pueda hacer el post
async def añadir_producto(producto: Producto):
    
    if type(buscar_producto(producto.nombre, producto.descripcion)) == Producto:
        raise HTTPException(status_code=409, detail = "El producto ya existe")
    
    #transformamos el usuario que recibimos a un diccionario
    producto_dict = producto.model_dump()
    #se elimina el campo id por si lo han introducido en el JSON por error
    del producto_dict["id"]
    #añadimos el usuario a nuestra BBDD
    #obtenemos con inserted_id el id que la BBDD ha generado para nuestro usuario
    id = db_client.local.productos.insert_one(producto_dict).inserted_id
    #añadimos el campo id a nuestro diccionario. hay que hacerle un cast
    #a string puesto que el id en BBDD se almacena como un objeto, no como un string
    producto_dict["id"] = str(id)
    
    #la respuesta de nuestro método es el propio usuario añadido de tipo producto
    return Producto(**producto_dict)

#método put para actualizar los datos de un producto existente
@router.put("/{id_producto}", response_model=Producto)
async def modificar_producto(id_producto: str, producto_nuevo: Producto):
    #se convierte el usuario a un diccionario
    producto_dict = producto_nuevo.model_dump()
    #eliminamos el id en caso de que venga porque no puede cambiar
    del producto_dict["id"]
    try:
        #buscamos el id en la BBDD y le pasamos el diccionario con los datos
        #a modificar del usuario
        db_client.local.productos.find_one_and_replace({"_id":ObjectId(id_producto)}, producto_dict)
        #buscamos el objeto en BBDD y lo retornamos, así comprobamos que efectivamente
        #se ha modificado
        return buscar_producto_id(id_producto)
    except:   
        #si no se encuentra lanzo una excepción
        raise HTTPException(status_code=404, detail="producto no encontrado")

#método para eliminar un producto
@router.delete("/{id_producto}", response_model=Producto)
async def eliminar_producto(id_producto: str):
    found = db_client.local.productos.find_one_and_delete({"_id":ObjectId(id_producto)})
    
    if not found:
        #si no se encuentra el id se elimina de la excepcion
        raise HTTPException(status_code=404, detail="producto no encontrado")
    return Producto(**producto_schema(found))