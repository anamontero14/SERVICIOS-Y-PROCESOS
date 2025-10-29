from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/producto", tags= ["producto"])

class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    idCliente: int

#lista de todos los productos
producto_list = [
    Producto(id=1, nombre="Tomate enlatado", descripcion="Tomate frito enlatado", precio=3.45, id_cliente=1),
    Producto(id=2, nombre="Aceite de oliva 500ml", descripcion="Aceite de oliva virgen extra", precio=6.99, id_cliente=2),
    Producto(id=3, nombre="Arroz 1kg", descripcion="Arroz largo tipo bomba", precio=1.85, id_cliente=3),
    Producto(id=4, nombre="Pasta integral 500g", descripcion="Pasta de trigo integral", precio=2.10, id_cliente=4),
    Producto(id=5, nombre="Leche entera 1L", descripcion="Leche fresca entera", precio=0.95, id_cliente=5),
    Producto(id=6, nombre="Azúcar 1kg", descripcion="Azúcar blanco refinado", precio=1.20, id_cliente=6),
    Producto(id=7, nombre="Café molido 250g", descripcion="Café 100% arábica molido", precio=4.50, id_cliente=7),
    Producto(id=8, nombre="Galletas integrales 300g", descripcion="Galletas integrales con avena", precio=2.75, id_cliente=8)
]

#buscar un producto
def buscar_producto(id: int):
    #recorre la lista de los productos
    for producto in producto_list:
        #si el id del producto actual es igual al id pasado por parámetros
        if productos.id == id:
            #en una variable se almacena el producto
            productos = producto
    
    if productos:
        return productos[0]
    raise HTTPException(status_code=404, detail="Producto no encontrado")

#obtener el siguiente id de la lista
def next_id():
    #almacenará el id máximo de la lista
    maximo = 0
    for producto in producto_list:
        #si el id del producto actual es mayor que lo almacenado en máximo
        if producto.id > maximo:
            #se iguala el máximio al id del producto actual
            maximo = producto.id
    #devuelve el máximo + 1
    return maximo + 1

#método get para obtener TODOS los productos
@router.get("/")
def productos():
    return producto_list

#método para obtener un producto con un id especifico y un atributo específico
@router.get("/query/")
def producto_atributo(id: int):
    return buscar_producto(id)

#método para buscar un producto con un id especifico
@router.get("/{id_producto}")
def producto_id(id_producto):
    return buscar_producto(id_producto)

#método post para añadir un nuevo cliente
@router.post("/", status_code=201, response_model=Producto)
def nuevo_producto(producto: Producto):
    #se le cambia el id introducido por el siguiente
    producto.id = next_id()
    #se añade a la lista
    producto_list.append(producto)
    #se retorna el producto
    return producto

#método put para actualizar un cliente en específico
@router.put("/{id_producto}", response_model=Producto)
def modificar_producto(id_producto: int, producto:Producto):
    #se busca el producto en especifico de la lista
    for producto_especifico in producto_list:
        #si el producto actual es igual que el id introducido por parámetros
        if producto_especifico.id == id_producto:
            #machaco el id del producto que se pasa y le asigno el actual
            producto.id = id_producto
            #se actualiza el producto
            producto_list[producto_especifico.id] = producto
            #se devuelve el producto modificado
            return producto
    #si no se encuentra lanza una excepcion
    raise HTTPException(status_code=404, detail="Producto no encontrado")

#método delete para elminar un producto de la lista
@router.delete("/{id_producto}")
def eliminar_producto(id_producto: int):
    #se recorre la lista
    for producto_especifico in producto_list:
        if producto_especifico.id == id_producto:
            #se elimina de la lista
            producto_list.remove(producto_especifico)
            #se devuelve el diccionario vacio
            return{}
    #si no se encuentra devuelve una excepcion
    raise HTTPException(status_code=404, detail="Producto no encontrado")
