from fastapi import APIRouter, Depends, HTTPException
from database import get_db_connection

router = APIRouter()

@router.get("/orders/:{order_id}")
def get_order_details(order_id: int, db=Depends(get_db_connection)):

    cursor = db.cursor()

    # se va a filtrar el estado del pago por el ultimo registro de actualizacion de pagos
    query = """
    SELECT 
        oc.id_orden_compra AS orderId,
        oc.client_id AS userId,
        od.product_id AS productId,
        od.quantity AS quantity,
        od.price AS price,
        eo.status AS status,
        TO_CHAR(oc.created_at, 'YYYY-MM-DD') AS createdAt
    FROM orden_compras oc
    LEFT JOIN orden_detalles od ON oc.id_orden_compra = od.order_id
    LEFT JOIN (
        SELECT order_id, status
        FROM pagos
        WHERE order_id = :order_id
        ORDER BY updated_at DESC
        FETCH FIRST 1 ROWS ONLY
    ) eo ON oc.id_orden_compra = eo.order_id
    WHERE oc.id_orden_compra = :order_id
    """

    cursor.execute(query, {"order_id": order_id})
    rows = cursor.fetchall()


    if not rows:
        raise HTTPException(status_code=404, detail="Order not found")

    # procesar datos
    order_info = {
        "orderId": rows[0][0],
        "userId": rows[0][1],
        "items": [],
        "totalAmount": 0.0,
        "status": rows[0][5],
        "createdAt": rows[0][6]
    }

    total_amount = 0
    for row in rows:
        if row[2] is not None:  # si tiene productos asociados
            order_info["items"].append({
                "productId": row[2],
                "quantity": row[3],
                "price": float(row[4])
            })
            total_amount += row[3] * row[4]  # cantidad * precio

    order_info["totalAmount"] = total_amount
    
    return order_info