from fastapi import APIRouter, Depends, HTTPException, Body, Path
from database import get_db_connection
from datetime import datetime

router = APIRouter()

@router.put("/orders/:{order_id}")
def get_order_details(
    order_id: int=Path(..., title="ID de la orden", ge=1),
    status_data: dict = Body(...), 
    db=Depends(get_db_connection)):
    
    cursor = db.cursor()

    # Verificar si la orden existe
    cursor.execute("SELECT id_orden_compra FROM orden_compras WHERE id_orden_compra = :order_id", {"order_id": order_id})
    existing_order = cursor.fetchone()

    if not existing_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Componer la consulta de actualización
    updated_at= datetime.now()

    #se va a cambiar el update_at en la tabla ordenes y el estado de la orden en la tabla pagos
    try:
        # actualizar la tabla orden_compras
        cursor.execute(
            "UPDATE orden_compras SET updated_at = :updated_at WHERE id_orden_compra = :order_id",
            {"updated_at": updated_at, "order_id": order_id}
        )

        # actualizar la tabla pagos
        cursor.execute(
            "UPDATE pagos SET status = :status, updated_at = :updated_at WHERE order_id = :order_id",
            {"status": status_data["status"], "updated_at": updated_at, "order_id": order_id}
        )

        db.commit()
        return {"status": 200, "message": "Estado de orden actualizada correctamente"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar la orden: {str(e)}")