from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Jugador(BaseModel):
    id: int
    nombre: str
    edad: int
    posicion: str
    nacionalidad: str
    salario: float
    idEquipo: int

jugadores_list = [
    Jugador(id=1, nombre="Lionel Messi", edad=37, posicion="Delantero", nacionalidad="Argentina", salario=75000000.0, idEquipo=10),
    Jugador(id=2, nombre="Kylian Mbappé", edad=26, posicion="Delantero", nacionalidad="Francia", salario=90000000.0, idEquipo=10),
    Jugador(id=3, nombre="Luka Modrić", edad=39, posicion="Centrocampista", nacionalidad="Croacia", salario=20000000.0, idEquipo=11),
    Jugador(id=4, nombre="Virgil van Dijk", edad=34, posicion="Defensa", nacionalidad="Países Bajos", salario=18000000.0, idEquipo=12),
    Jugador(id=5, nombre="Thibaut Courtois", edad=33, posicion="Portero", nacionalidad="Bélgica", salario=15000000.0, idEquipo=11),
    Jugador(id=6, nombre="Erling Haaland", edad=25, posicion="Delantero", nacionalidad="Noruega", salario=85000000.0, idEquipo=13),
    Jugador(id=7, nombre="Kevin De Bruyne", edad=34, posicion="Centrocampista", nacionalidad="Bélgica", salario=60000000.0, idEquipo=13),
    Jugador(id=8, nombre="Pedri González", edad=22, posicion="Centrocampista", nacionalidad="España", salario=35000000.0, idEquipo=14),
    Jugador(id=9, nombre="Vinícius Jr.", edad=25, posicion="Delantero", nacionalidad="Brasil", salario=70000000.0, idEquipo=11),
    Jugador(id=10, nombre="Jude Bellingham", edad=22, posicion="Centrocampista", nacionalidad="Inglaterra", salario=65000000.0, idEquipo=11)
]


#función para encontrar un jugador por id
def buscar_jugador(id: int):
    jugadores = [jugador for jugador in jugadores_list if jugador.id == id]

    if jugadores:
        return jugadores[0]
    raise HTTPException(status_code=404, detail="Player not found")

#método para devolver el id por el que empezará un supuesto objeto añadido
def siguiente_id():
    return (max(jugadores_list, key=id).id+1)

#devuelve todos los jugadores
@app.get("/jugadores")
def jugadores ():
    return jugadores_list

#devuelve el jugador con el id correspondiente
@app.get("/jugadores/{id_jugador}")
#el nombre del parámetro y el nombre del {} tiene que ser el MISMO
def jugador_id(id_jugador: int):
    return buscar_jugador(id_jugador)

#añade un nuevo jugador a la lista
@app.post("/jugadores", status_code=201, response_model=Jugador)
def nuevo_jugador(jugador: Jugador):
    #se le cambia el id que llega por el siguiente que corresponde
    jugador.id = siguiente_id()

    #se añade a la lista de los jugadores
    jugadores_list.append(jugador)

    #returna el propio objeto
    return jugador

#actualiza los datos de un jugador existente
@app.put("/jugadores/{id}", response_model=Jugador)
def modificar_jugador(id: int, jugador: Jugador):
    #for para que devuelva el índice y el usuario
    for index, jugador_guardado in enumerate(jugadores_list):
        #si el jugador que hay en la lista tiene el mismo
        #id que el que se le pasa por parámetros
        if jugador_guardado.id == id:
            #machaco el id que tenga el objeto jugador y le asigno el
            #que se le pasa por parámetro
            jugador.id = id
            #en la lista actualizo al jugador
            jugadores_list[index] = jugador
            #se retorna el jugador modificado
            return jugador
        
    #si no se encuentra lanza una excepción
    raise HTTPException(status_code=404, detail="Jugador no encontrado")

#método delete para poder eliminar a un jugador de la lista
@app.delete("/jugadores/{id}")
#se le pasa el id del jugador a eliminar
def eliminar_jugador(id: int):
    #se recorre la lista de los jugadores
    for jugador_guardado in jugadores_list:
        #si el id del jugador actual es igual al id pasado por parámetro
        if jugador_guardado.id == id:
            #se elimina al jugador de la lista
            jugadores_list.remove(jugador_guardado)
            #se devuelve el diccionario vacío
            return {}
    
    #si no se encuentra el id del jugador a eliminar lanza una excepcion
    raise HTTPException(status_code=404, detail="Jugador no encontrado")