from fastapi import FastAPI
from routers import cliente, producto
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(cliente.router)
app.include_router(producto.router)

#la imagen
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def inicio():
    return {"Hello world"}