def cliente_schema(cliente) -> dict:
    #el id en la BBDD es _id
    return {"id" : str(cliente["_id"]),
            "nombre": cliente["nombre"],
            "apellidos": cliente["apellido"],
            "telefono": cliente["telefono"],
            "email": cliente["email"]
            }

def clientes_schema(clientes) -> list:
    return [cliente_schema(cliente) for cliente in clientes]