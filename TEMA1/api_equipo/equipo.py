from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#entidad user
class Equipo(BaseModel):
    id: int
    nombre: str
    ciudad: str
    año_fundacion: str
    estadio: str

equipo_list = [Equipo(id=1 ,nombre="Equipo1", ciudad="Sevilla", año_fundacion="1945", estadio="Estadio1"),
              Equipo(id=2 ,nombre="Equipo2", ciudad="Madrid", año_fundacion="1934", estadio="Estadio23"),
              Equipo(id=3 ,nombre="Equipo3", ciudad="Málaga", año_fundacion="2000", estadio="Estadio55")]

@app.get("/equipos")
def equipos():
    return equipo_list

@app.get("/equipos/{id_equipo}")
def get_user(id_equipo: int):
    equipos = [user for user in equipo_list if user.id == id_equipo]

    return equipos[0] if equipos else {"Error" : "User not found"}