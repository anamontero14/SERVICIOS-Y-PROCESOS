def producto_schema(producto) -> dict:
    #el id en la BBDD es _id
    return {"id" : str(producto["_id"]),
            "nombre": producto["nombre"],
            "descripcion": producto["descripcion"],
            "precio": producto["precio"],
            "idCliente": producto["idCliente"]
            }

def producto_schema(productos) -> list:
    return [producto_schema(producto) for producto in productos]