from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/equipo", tags= ["equipos"])

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


#método para buscar equipos
def buscar_equipos(id: int):
    equipos = [equipo for equipo in equipo_list if equipo.id == id]

    if equipos:
        return equipos[0]
    raise HTTPException(status_code=404, detail="Equipo no encontrado")

#método para indicar el siguiente id
def siguiente_id():
    #devuelve el usuario con la id máxima y a este le suma 1 a su id
    return max(equipo_list, key=lambda x: x.id).id + 1

#devuelve todos los equipos
@router.get("/")
def equipos():
    return equipo_list

@router.get("/{id_equipo}")
def get_equipo(id_equipo: int):
    return buscar_equipos(id_equipo)

#método post para añadirlo a la lista
@router.post("/", status_code=201, response_model=Equipo)
#recibe un equipo de tipo equipo para meterlo a la lista
def add_equipo(equipo: Equipo):
    #al equipo pasado por parámetro se le asigna el siguiente id
    equipo.id = siguiente_id()
    #finalmente se añade a la lista
    equipo_list.append(equipo)
    #devuelve el mismo equipo
    return equipo

#método put para actualizar un usuario concreto
@router.put("/{id}", response_model=Equipo)
#se le pasará el id que tiene el equipo y sus datos a actualizar
def modificar_equipo(id: int, equipo: Equipo):
    #for para que devuelva el índice y el usuario
    for index, equipo_guardado in enumerate(equipo_list):
        #si el equipo que hay en la lista tiene el mismo
        #id que el que se le pasa por parámetros
        if equipo_guardado.id == id:
            #machaco el id que tenga el objeto equipo y le asigno el
            #que se le pasa por parámetro
            equipo.id = id
            #en la lista actualizo al equipo
            equipo_list[index] = equipo
            #se retorna el equipo modificado
            return equipo
        
    #si no se encuentra lanza una excepción
    raise HTTPException(status_code=404, detail="Equipo no encontrado")

#método delete para poder eliminar a un equipo de la lista
@router.delete("/{id}")
#se le pasa el id del equipo a eliminar
def eliminar_equipo(id: int):
    #se recorre la lista de los equipos
    for equipo_guardado in equipo_list:
        #si el id del equipo actual es igual al id pasado por parámetro
        if equipo_guardado.id == id:
            #se elimina al equipo de la lista
            equipo_list.remove(equipo_guardado)
            #se devuelve el diccionario vacío
            return {}
    
    #si no se encuentra el id del equipo a eliminar lanza una excepcion
    raise HTTPException(status_code=404, detail="Equipo no encontrado")