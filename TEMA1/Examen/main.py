from fastapi import FastAPI
from routers import alumnos, colegios, auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(alumnos.router)
app.include_router(colegios.router)
app.include_router(auth_users.router)

@app.get("/")
def inicio():
    return {"Bienvenid@ a la base de datos"}