from fastapi import FastAPI

#enpoints de clientes
from routes.clientes.clientes import router as clientes_router
from routes.clientes.autenticacion import router as autenticacion_router
from routes.clientes.obtenerDatosEsp import router as obtenerDatosEsp_router
from routes.clientes.actualizar import router as actualizar_router
from routes.clientes.eliminar import router as eliminar_router


app = FastAPI()


app.include_router(clientes_router)
app.include_router(autenticacion_router)
app.include_router(obtenerDatosEsp_router)
app.include_router(actualizar_router)
app.include_router(eliminar_router)


@app.get("/")
def read_root():
    return {"message": "API con Oracle funcionando"}
