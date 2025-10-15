from fastapi import FastAPI
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

@app.get("/users/{id_user}")
def get_user(id_user: int):
    users = [user for user in users_list if user.id == id_user]

    return users[0] if users else {"Error" : "User not found"}