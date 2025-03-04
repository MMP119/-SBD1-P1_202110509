from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db_connection
from pydantic import BaseModel, Field
import bcrypt



router = APIRouter()



# modelo para iniciar sesión
class loginBase(BaseModel): #será el national_document, ya que es único
    username: int = Field(..., description="username no puede estar vacío")
    password: str = Field(..., min_length=1, description="La contraseña no puede estar vacía")



#funcion para obtener el id de cliente y retornarlo como un id de sesion
def obtener_id_cliente(db, credenciales: loginBase):

    cursor = db.cursor()

    #verificar si el correo o el nombre de usuario ya existen
    query = """
        SELECT COUNT(*) FROM clientes
        WHERE national_document = :national_document
    """
    cursor.execute(query, {"national_document": credenciales.username})
    count = cursor.fetchone()[0]

    if count == 0:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    #comparar la contraseña ingresada con la contraseña hasheada
    query = """
        SELECT password FROM clientes
        WHERE national_document = :national_document
    """
    cursor.execute(query, {"national_document": credenciales.username})
    hashed_password = cursor.fetchone()[0]
    if not bcrypt.checkpw(credenciales.password.encode('utf-8'), hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    #obtener el id de cliente
    query = """
        SELECT client_id FROM clientes
        WHERE national_document = :national_document
    """
    cursor.execute(query, {"national_document": credenciales.username})
    client_id = cursor.fetchone()[0]
    return client_id



# Endpoint loguear a un cliente
@router.post("/users/login")
def loguear(cliente_json: loginBase, db=Depends(get_db_connection)):

    client_id = obtener_id_cliente(db, cliente_json)

    return {"status":200,"message": "User authenticated", "sessionId": client_id}
