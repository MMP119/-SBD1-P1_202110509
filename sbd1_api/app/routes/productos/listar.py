from fastapi import APIRouter, Depends, HTTPException
from database import get_db_connection

router = APIRouter()

@router.get("/products", response_model=dict)
def list_products(db=Depends(get_db_connection)):
    cursor = db.cursor()

    #consultar productos y obtener su stock
    query = """
        SELECT p.id_producto, p.name, p.price, COALESCE(SUM(i.quantity), 0) as stock
        FROM productos p
        LEFT JOIN inventarios i ON p.id_producto = i.product_id
        GROUP BY p.id_producto, p.name, p.price
    """
    
    cursor.execute(query)
    productos = cursor.fetchall()

    #verificar si hay productos
    if not productos:
        raise HTTPException(status_code=404, detail="No hay productos disponibles")

    #formatear la respuesta en JSON
    productos_list = [
        {"id": row[0], "name": row[1], "price": row[2], "stock": row[3]}
        for row in productos
    ]

    return {"products": productos_list}