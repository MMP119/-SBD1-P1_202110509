from fastapi import FastAPI, Depends
import cx_Oracle
from database import get_db_connection
from routes.clientes.clientes import router as clientes_router
from routes.clientes.autenticacion import router as autenticacion_router
from routes.clientes.obtenerDatosEsp import router as obtenerDatosEsp_router

app = FastAPI()


app.include_router(clientes_router)
app.include_router(autenticacion_router)
app.include_router(obtenerDatosEsp_router)


@app.get("/")
def read_root():
    return {"message": "API con Oracle funcionando"}
