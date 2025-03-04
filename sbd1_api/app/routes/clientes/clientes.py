from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db_connection
import cx_Oracle
from pydantic import BaseModel
import bcrypt



router = APIRouter()



# modelo para validar JSON de Cliente
class ClienteBase(BaseModel):
    national_document: int
    name: str
    lastname: str
    phone: str
    email: str
    active: str
    confirmed_email: str
    password: str



# función para verificar si el correo o el nombre de usuario ya existen
def verificar_usuario_existe(db, email: str, national_document: int):
    cursor = db.cursor()
    query = """
        SELECT COUNT(*) FROM clientes
        WHERE email = :email OR national_document = :national_document
    """
    cursor.execute(query, {"email": email, "national_document": national_document})
    count = cursor.fetchone()[0]
    return count > 0



# función para hashear la contraseña
def hashear_contrasena(password: str) -> str:
    # Hashear la contraseña utilizando bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')



# insertar cliente en la base de datos
def insert_cliente(db, cliente: ClienteBase):
    cursor = db.cursor()
    
    # validar 'active' y 'confirmed_email' para asegurarse que sean 'TRUE' o 'FALSE'
    if cliente.active not in ('TRUE', 'FALSE'):
        raise HTTPException(status_code=400, detail="El valor de 'active' debe ser 'TRUE' o 'FALSE'")
    if cliente.confirmed_email not in ('TRUE', 'FALSE'):
        raise HTTPException(status_code=400, detail="El valor de 'confirmed_email' debe ser 'TRUE' o 'FALSE'")

    # verificar si el correo o el documento nacional ya existen
    if verificar_usuario_existe(db, cliente.email, cliente.national_document):
        raise HTTPException(status_code=409, detail="El correo electrónico o documento nacional ya existe")

    # Hashear la contraseña
    hashed_password = hashear_contrasena(cliente.password)

    query = """
        INSERT INTO clientes (national_document, name, lastname, phone, email, active, confirmed_email, password)
        VALUES (:national_document, :name, :lastname, :phone, :email, :active, :confirmed_email, :password)
        RETURNING client_id INTO :client_id
    """
    client_id = cursor.var(cx_Oracle.NUMBER)
    cursor.execute(query, {**cliente.dict(), "password": hashed_password, "client_id": client_id}) 
    db.commit()
    return int(client_id.getvalue()[0])




# Endpoint para crear cliente
@router.post("/users", status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente_json: ClienteBase, db=Depends(get_db_connection)):
    # Crear cliente en la base de datos
    client_id = insert_cliente(db, cliente_json)
    
    return {"status":200, "message": "Usuario creado con éxito", "client_id": client_id}
