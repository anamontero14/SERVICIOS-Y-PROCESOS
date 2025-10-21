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

@app.get("/users/{id}")
def get_user(id: int):
    return search_user(id)

@app.get("/users/")
def get_user(id: int):
    return search_user(id)