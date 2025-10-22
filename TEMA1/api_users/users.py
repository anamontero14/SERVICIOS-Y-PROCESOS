from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


#entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_list = [User(id=1 ,name="Paquín", surname="Rubito", age=56),
              User(id=2 ,name="Joaquín", surname="Chami", age=35),
              User(id=3, name="Benito", surname="Menganito", age=54),
              User(id=4, name="Fulano", surname="Mengano", age=23)]

@app.get("/users")
def users():
    return users_list

def search_user(id: int):
    """buscamos usuario por id en la lista, devuelve
    una lista vacía si no encuentra nada
    devuelve una lista con el usuario encontrado"""
    users = [user for user in users_list if user.id == id]

    """comprueba que la lista no está vacía y si no lo está devuelve
    la primera posición de la lista, si es falso entonces
    devuelve un diccionario con el error"""
    #return users[0] if users else {"Error" : "User not found"}

    if users:
        return users[0]
    raise HTTPException(status_code=404, detail="User not found")

def next_id():
    #devuelve el usuario con la id máxima y después le suma 1 para pasar al siguiente id
    #para la persona a añadir
    return (max(users_list, key=id).id+1)

@app.get("/users/{id}")
def get_user(id: int):
    return search_user(id)

@app.post("/users", status_code=201, response_model=User)
#recibe un usuario de tipo usuario para meter a la lista
def add_user(user : User):
    #al usuario introducido se le asigna el id correcto
    user.id = next_id()
    #se añade el usuario a la lista
    users_list.append(user)
    #se devuelve el usuario atualizado
    return user

@app.put("/users/{id}", response_model=User)
def modify_user(id: int, user: User):
    #for para que devuelva el índice y el usuario
    for index, saved_user in enumerate(users_list):
        #si el usuario que yo tengo en la lista es igual
        #al id que recibo
        if saved_user.id == id:
            #machaco el id del usuario por el que se pasa por parámetros
            user.id = id
            #en la lista de users actualizo el user
            users_list[index] = user
            #y se retorna
            return user
    
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{id}")
def delete_user(id:int):
    #recorre la lista
    for saved_user in users_list:
        #si los ids de la lista de usuarios y el que se pasa coinciden
        if saved_user.id == id:
            #se elimina de la lista el usuario
            users_list.remove(saved_user)
            #se devuelve el diccionario vacío
            return {}
    #si no se encuentra devuelve una excepcion
    raise HTTPException(status_code=404, detail="User not found")