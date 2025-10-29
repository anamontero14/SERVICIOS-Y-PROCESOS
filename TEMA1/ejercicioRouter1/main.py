from fastapi import FastAPI
from routers import equipo, jugador
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(equipo.router)
app.include_router(jugador.router)

#la imagen
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def inicio():
    return {"Hello world"}