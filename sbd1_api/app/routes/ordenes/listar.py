from fastapi import APIRouter, Depends
from database import get_db_connection

router = APIRouter()

@router.get("/orders")
def list_orders(db=Depends(get_db_connection)):

    cursor = db.cursor()

    query = """
        SELECT 
            oc.id_orden_compra AS orderId,
            oc.client_id AS userId,
            COALESCE(SUM(od.price * od.quantity), 0) AS totalAmount,
            eo.status AS status,
            TO_CHAR(oc.created_at, 'YYYY-MM-DD') AS createdAt
        FROM orden_compras oc
        LEFT JOIN orden_detalles od ON oc.id_orden_compra = od.order_id
        LEFT JOIN pagos eo ON oc.id_orden_compra = eo.order_id
        GROUP BY oc.id_orden_compra, oc.client_id, eo.status, oc.created_at
        ORDER BY oc.created_at DESC
    """

    cursor.execute(query)
    orders = [
        {
            "orderId": row[0],
            "userId": row[1],
            "totalAmount": float(row[2]),  
            "status": row[3],
            "createdAt": row[4]
        }
        for row in cursor.fetchall()
    ]
    
    return {"orders": orders}
