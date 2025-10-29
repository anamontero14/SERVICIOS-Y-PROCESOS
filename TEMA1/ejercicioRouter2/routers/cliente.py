from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/clientes", tags= ["clientes"])

class Cliente(BaseModel):
    id: int
    nombre: str
    apellidos: str
    telefono: int
    email: str

#listado de los clientes
clientes_list = [
    Cliente(id=1, nombre="Juan", apellidos="Pérez Martínez", telefono=344115423, email="juan@email.com"),
    Cliente(id=2, nombre="María", apellidos="González Ruiz", telefono=611223344, email="maria.gonzalez@example.com"),
    Cliente(id=3, nombre="Luis", apellidos="Fernández López", telefono=655998877, email="luis.fernandez@example.com"),
    Cliente(id=4, nombre="Ana", apellidos="Sánchez Ortega", telefono=622334455, email="ana.sanchez@example.com"),
    Cliente(id=5, nombre="Carlos", apellidos="Muñoz Pérez", telefono=633445566, email="carlos.munoz@example.com"),
    Cliente(id=6, nombre="Lucía", apellidos="Ramírez Soto", telefono=600112233, email="lucia.ramirez@example.com"),
    Cliente(id=7, nombre="Pablo", apellidos="Vázquez Romero", telefono=644556677, email="pablo.vazquez@example.com"),
    Cliente(id=8, nombre="Elena", apellidos="Torres Hidalgo", telefono=699887766, email="elena.torres@example.com")
]


#funcion para encontrar un cliente por id
def buscar_cliente(id: int):
    clientes = [clientes for clientes in clientes_list if clientes.id == id]

    if clientes:
        return clientes[0]
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

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
def clientes():
    return clientes_list

#método para devolver un cliente en específico dependiendo de un atributo
@router.get("/query/")
def clientes(id: int):
    return buscar_cliente(id)

#método para devolver un cliente con un id específico
@router.get("/{id_cliente}")
def cliente_id(id_cliente: int):
    return buscar_cliente(id_cliente)

#método post para añadir un nuevo cliente a la lista
@router.post("/", status_code= 201, response_model=Cliente)
def añadir_cliente(cliente: Cliente):
    #se le cambia el id que le llegue por el siguiente id de la lista
    cliente.id = next_id()
    #se añade a la lista de los clientes
    clientes_list.append(cliente)
    #devuelvo el propio objeto
    return cliente

#método put para actualizar los datos de un cliente existente
@router.put("/{id_cliente}", response_model=Cliente)
def modificar_cliente(id_cliente: int, cliente: Cliente):
    #for para que devuelva el índice y el usuario
    for index, cliente_guardado in enumerate(clientes_list):
        #si el jugador que hay en la lista tiene el mismo
        #id que el que se le pasa por parámetros
        if cliente_guardado.id == id_cliente:
            #machaco el id que tenga el objeto jugador y le asigno el
            #que se le pasa por parámetro
            cliente.id = id_cliente
            #en la lista actualizo al jugador
            clientes_list[index] = cliente
            #se retorna el jugador modificado
            return cliente
        
    #si no se encuentra lanzo una excepción
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

#método para eliminar un cliente
@router.delete("/{id_cliente}")
def eliminar_cliente(id_cliente: int):
    #se recorre la lisa para encontrar al cliente a eliminar
    for cliente in clientes_list:
        #si el id del cliente actual es igual al id que se pasa por parámetros
        if cliente.id == id_cliente:
            #se elimina de la lista
            clientes_list.remove(cliente)
            #se devuelve el diccionario vacío
            return {}
        
    #si no se encuentra el id se elimina de la excepcion
    raise HTTPException(status_code=404, detail="Cliente no encontrado")