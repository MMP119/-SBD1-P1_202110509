from fastapi import APIRouter, HTTPException, Path, Depends
from database import get_db_connection

router = APIRouter()

# eliminar un usuario
@router.delete("/users/:{client_id}")
def delete_user(
    client_id: int = Path(..., title="ID del cliente", ge=1),
    db=Depends(get_db_connection)
):
    # ver que exista
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes WHERE client_id = :id", {"id": client_id})
    cliente_db = cursor.fetchone()

    if not cliente_db[0]: 
        raise HTTPException(status_code=404, detail="El cliente no existe")

    # Eliminamos al usuario de la base de datos
    cursor.execute("DELETE FROM clientes WHERE client_id = :id", {"id": client_id})

    db.commit()  # guarda los cambios

    return {"status": 200, "message": "User deleted successfully"}
