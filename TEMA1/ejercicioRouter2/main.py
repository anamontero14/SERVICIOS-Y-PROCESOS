from fastapi import FastAPI
from routers import auth_users, cliente_db, producto_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
#app.include_router(cliente.router)
app.include_router(producto_db.router)
app.include_router(auth_users.router)
app.include_router(cliente_db.router)

#la imagen
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def inicio():
    return {"Bienvenid@ a la base de datos"}