from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db_connection

router = APIRouter()


# Endpoint para obtener la info de un usuario en específico por su id sin exponer la contraseña
@router.get("/users/:{client_id}")
def obtener_cliente(client_id: int, db=Depends(get_db_connection)):

    cursor = db.cursor()

    query = """
        SELECT COUNT(*) FROM clientes
        WHERE client_id = :client_id
    """
    cursor.execute(query, {"client_id": client_id})
    count = cursor.fetchone()[0]
    
    if count == 0:
        raise HTTPException(status_code=404, detail="El usuario no existe")


    query = """
        SELECT national_document, name, lastname, phone, email, active, confirmed_email, created_at, updated_at
        FROM clientes
        WHERE client_id = :client_id
    """
    cursor.execute(query, {"client_id": client_id})
    cliente = cursor.fetchone()
    
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return dict(zip(["national_document", "name", "lastname", "phone", "email", "active", "confirmed_email", "created_at","update_at"], cliente))


