from fastapi import APIRouter, Depends, HTTPException
from database import get_db_connection

router = APIRouter()

@router.post("/orders", status_code=201)
def create_order(order: dict, db=Depends(get_db_connection)):
    
    cursor = db.cursor()

    #obtener datos del request
    user_id = order.get("userId")
    location_id = order.get("locationId")
    items = order.get("items")
    payment_method = order.get("paymentMethod")

    #verificar que todos los datos estén presentes
    if not user_id or not location_id or not items or not payment_method:
        raise HTTPException(status_code=400, detail="Datos incompletos")

    #ver que exista el usuario
    cursor.execute("SELECT client_id FROM clientes WHERE client_id = :user_id", {"user_id": user_id})
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    #verificar productos y calcular total
    total_amount = 0
    product_details = []

    for item in items:
        product_id = item["productId"]
        quantity = item["quantity"]

        cursor.execute("SELECT price FROM productos WHERE id_producto = :product_id", {"product_id": product_id})
        product = cursor.fetchone()

        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {product_id} no encontrado")

        price = product[0]
        total_amount += price * quantity
        product_details.append((product_id, quantity, price))

    #variable para almacenar el ID devuelto
    order_id_var = cursor.var(int)

    #insertar la orden y retornar el ID
    insert_order = """
        INSERT INTO orden_compras (client_id, location_id, created_at, updated_at)
        VALUES (:client_id, :location_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        RETURNING id_orden_compra INTO :order_id
    """

    cursor.execute(insert_order, {"client_id": user_id, "location_id": location_id, "order_id": order_id_var})

    #valor de la variable
    order_id = order_id_var.getvalue()[0]

    #insertar los productos en orden_detalles
    for product_id, quantity, price in product_details:
        insert_order_details = """
            INSERT INTO orden_detalles (order_id, product_id, quantity, price, created_at, updated_at)
            VALUES (:order_id, :product_id, :quantity, :price, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        cursor.execute(insert_order_details, {"order_id": order_id, "product_id": product_id, "quantity": quantity, "price": price})

    #isertar el pago en pagos
    insert_payment = """
        INSERT INTO pagos (order_id, payment_method, status, created_at, updated_at)
        VALUES (:order_id, :payment_method, 'processing', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """
    cursor.execute(insert_payment, {"order_id": order_id, "payment_method": payment_method})

    db.commit()

    return {
        "status": "success",
        "message": "Order created successfully",
        "orderId": order_id,
        "totalAmount": total_amount,
        "orderStatus": "processing"
    }
