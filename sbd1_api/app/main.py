from fastapi import FastAPI, Depends
import cx_Oracle
from database import get_db_connection
from routes.clientes import router as clientes_router

app = FastAPI()


app.include_router(clientes_router)


@app.on_event("startup")
async def startup_event():
    try:
        await get_db_connection()
    except Exception as e:
        print(e)


@app.get("/")
def read_root():
    return {"message": "API con Oracle funcionando"}
