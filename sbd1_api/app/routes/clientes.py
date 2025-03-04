from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from database import get_db_connection
import cx_Oracle
import csv
import io
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Modelos para validar JSON
class ClienteBase(BaseModel):
    id_nacional: int
    nombre: str
    apellido: str
    telefono: str
    email: str
    activo: str
    correo_confirmado: str
    contrasena: str

class DireccionBase(BaseModel):
    direccion: str

class MetodoPagoBase(BaseModel):
    metodo_pago: str

class ClienteCreate(ClienteBase):
    direcciones: List[DireccionBase]
    metodos_pago: List[MetodoPagoBase]

# Insertar cliente en la base de datos
def insert_cliente(db, cliente: ClienteBase):
    cursor = db.cursor()
    query = """
        INSERT INTO clientes (id_nacional, nombre, apellido, telefono, email, activo, correo_confirmado, contrasena)
        VALUES (:id_nacional, :nombre, :apellido, :telefono, :email, :activo, :correo_confirmado, :contrasena)
        RETURNING id_cliente INTO :id_cliente
    """
    id_cliente = cursor.var(cx_Oracle.NUMBER)
    cursor.execute(query, {**cliente.dict(), "id_cliente": id_cliente})
    db.commit()
    return int(id_cliente.getvalue()[0])

# Insertar direcciones

def insert_direcciones(db, id_cliente, direcciones: List[DireccionBase]):
    cursor = db.cursor()
    for direccion in direcciones:
        cursor.execute(
            "INSERT INTO direcciones (id_cliente, direccion) VALUES (:id_cliente, :direccion)",
            {"id_cliente": id_cliente, "direccion": direccion.direccion},
        )
    db.commit()

# Insertar métodos de pago
def insert_metodos_pago(db, id_cliente, metodos_pago: List[MetodoPagoBase]):
    cursor = db.cursor()
    for metodo in metodos_pago:
        cursor.execute(
            "INSERT INTO metodos_pago (id_cliente, metodo_pago) VALUES (:id_cliente, :metodo_pago)",
            {"id_cliente": id_cliente, "metodo_pago": metodo.metodo_pago},
        )
    db.commit()

# Endpoint para recibir JSON o CSV
@router.post("/clientes")
def crear_clientes(
    db=Depends(get_db_connection),
    archivo: Optional[UploadFile] = File(None),
    cliente_json: Optional[ClienteCreate] = None,
):
    if archivo:
        # Procesar CSV
        contenido = archivo.file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(contenido))
        for fila in reader:
            cliente = ClienteBase(
                id_nacional=int(fila["national_document"]),
                nombre=fila["name"],
                apellido=fila["lastname"],
                telefono=fila["phone"],
                email=fila["email"],
                activo=fila["active"],
                correo_confirmado=fila["confirmed_email"],
                contrasena=fila["password"],
            )
            id_cliente = insert_cliente(db, cliente)
        return {"message": "Clientes cargados desde CSV"}
    elif cliente_json:
        # Procesar JSON
        id_cliente = insert_cliente(db, cliente_json)
        insert_direcciones(db, id_cliente, cliente_json.direcciones)
        insert_metodos_pago(db, id_cliente, cliente_json.metodos_pago)
        return {"message": "Cliente registrado con éxito", "id_cliente": id_cliente}
    else:
        raise HTTPException(status_code=400, detail="Debe enviar JSON o un archivo CSV")
