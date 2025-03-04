from fastapi import APIRouter, HTTPException, Body, Path, Depends
from database import get_db_connection
from datetime import datetime

router = APIRouter()


#modificar los datos de un cliente (excepto la contraseña)
@router.put("/users/:{client_id}")
def update_client(
    client_id: int = Path(..., title="ID del cliente", ge=1),
    client_data: dict = Body(...),
    db=Depends(get_db_connection)
    ):
    
    #verificamos que el usuario exista
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes WHERE id = :id", {"id": client_id})
    cliente_db = cursor.fetchone()

    if not cliente_db:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    

    # verificar si se intenta actualizar la contraseña (campo no permitido)
    if "password" in client_data:
        raise HTTPException(status_code=400, detail="No se puede actualizar la contraseña desde este endpoint")


    #componer la consulta de actualizacion
    set_clause = ", ".join([f"{key} = :{key}" for key in client_data.keys()])
    client_data["updated_at"] = datetime.now() #para la fecha de actualizacion

    update_query = f"""
        UPDATE clientes
        SET {set_clause}, updated_at = :updated_at
        WHERE client_id = :id
    """

    # se ejecuta la actualizacion
    client_data["id"] = client_id
    cursor.execute(update_query, client_data)
    db.commit()

    #confirmar la actualizacion
    return {"status": 200,"message": "User updated successfully"}