from fastapi import FastAPI
from app.routes import users

app = FastAPI(title="SBD1 API", version="0.1.0")

app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "prueba de fastapi!"}