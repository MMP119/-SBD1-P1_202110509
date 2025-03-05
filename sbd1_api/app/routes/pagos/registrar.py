from fastapi import APIRouter, Depends, HTTPException
from database import get_db_connection

router = APIRouter()

@router.get("/payments")
def get_payments(db=Depends(get_db_connection)):
    
    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT 
                id_pago AS payment_Id,
                order_id AS order_Id,
                payment_method AS method,
                status,
                TO_CHAR(created_at, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS createdAt
            FROM pagos
        """)
        payments = cursor.fetchall()

        #pasar a lista de diccionarios
        payments_list = [
            {
                "payment_Id": row[0],
                "order_Id": row[1],
                "method": row[2],
                "status": row[3],
                "createdAt": row[4]
            }
            for row in payments
        ]

        return {"payments": payments_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar pagos: {str(e)}")
