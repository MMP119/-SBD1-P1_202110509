from fastapi import APIRouter, Depends, HTTPException, Body
from database import get_db_connection
from datetime import datetime

router = APIRouter()

@router.post("/payments")
def register_payment(
    payment_data: dict = Body(...), 
    db=Depends(get_db_connection)
):
    cursor = db.cursor()

    # Verificar si la orden de compra existe
    cursor.execute("SELECT id_orden_compra FROM orden_compras WHERE id_orden_compra = :order_id", {"order_id": payment_data["orderId"]})
    existing_order = cursor.fetchone()

    if not existing_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    try:
        # Insertar el pago en la tabla pagos y retornar el id del pago
        payment_id = cursor.var(int)
        cursor.execute("""
            INSERT INTO pagos (order_id, payment_method, status, created_at, updated_at)
            VALUES (:order_id, :method, :status, :created_at, :updated_at)
            RETURNING id_pago INTO :payment_id
        """, {
            "order_id": payment_data["orderId"],
            "method": payment_data["method"],
            "status": payment_data["status"],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "payment_id": payment_id
        })

        db.commit()
        return {"status": 200, "message": "Payment registered successfully", "paymentId": payment_id.getvalue()}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar el pago: {str(e)}")
