from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse
import bcrypt
from typing import Dict

class User(BaseModel):
    username: str
    email: str
    password: str
    phone: str

class Login_Request(BaseModel):
    username: str
    password: str


router = APIRouter() # sirve para definir rutas


fake_db = [
    {"username": "johndoe", "email": "john@gmail.com", "password": "password", "phone": "1234567890"},
    {"username": "mario", "email": "mario@gmail.com", "password": "123", "phone": "456"},
]

@router.post("/users", status_code=201)  # CREAR UN NUEVO USUARIO EN LA PLATAFORMA, un request (JSON)
async def create_user(request: Request):

    body = await request.json() # se obtiene el cuerpo de la solicitud para convertirlo en un diccionario

    try:
        user = User(**body)  # pydantic valida el JSON

    except ValidationError as e:

        raise HTTPException(status_code=400, detail="Datos incompletos o incorrectos.")
    
    #Verificar si ya existe el username o email en la base de datos
    for user_db in fake_db:
        if user_db["username"] == user.username or user_db["email"] == user.email:
            raise HTTPException(status_code=409, detail="El username o email ya existe.")
        
    #si todo va bien, hasheamos la contraseña con bcrypt
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'),bcrypt.gensalt()) #convertimos a bytes la contraseña y generamos un salt aleatorio

    user_dict = user.dict() #convertimos el objeto user a un diccionario de python, así podemos cambiar directamente los campos 

    user_dict["password"] = hashed_password.decode('utf-8') #pasamos el hash a string para guardarlo en la base de datos

    fake_db.append(user_dict) #el body tiene la estructura de un diccionario que debe tener los campos de User

    return JSONResponse(content={"status":"success", "message": "User created successfully"}, status_code=201)



@router.post("/users/login") # LOGIN DE USUARIO, un request (JSON)
async def login_user(request: Request):

    body = await request.json()

    try:
        login_data = Login_Request(**body)
    
    except ValidationError as e:

        raise HTTPException(status_code=400, detail="Datos incompletos o incorrectos.")
    
    # Verificar si el usuario existe
    user = next((u for u in fake_db if u["username"] == login_data.username), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    # Comparar la contraseña con el hash almacenado
    if not bcrypt.checkpw(login_data.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta.")
    
    # Simular un ID de sesión
    session_id = "abc123"  # Esto podría ser un token JWT o algo similar
    
    return JSONResponse(content={"status": "success", "message": "User authenticated", "sessionId": session_id}, status_code=200)
