from fastapi import FastAPI
from sbd1_api.app.routes import clientes

app = FastAPI(title="SBD1 API", version="0.1.0")

app.include_router(clientes.router)


@app.get("/")
def read_root():
    return {"message": "prueba de fastapi!"}