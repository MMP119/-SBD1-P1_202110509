from fastapi import APIRouter, Depends, HTTPException
from database import get_db_connection

router = APIRouter()

@router.get("/products/:{id_producto}")
def dellate(id_producto:int ,db=Depends(get_db_connection)):
    cursor = db.cursor()

    query = """
        SELECT COUNT(*) FROM productos
        WHERE id_producto = :id_producto
    """
    cursor.execute(query, {"id_producto": id_producto})
    count = cursor.fetchone()[0]

    if count == 0:
        raise HTTPException(status_code=404, detail="El producto no existe")
    
    query = """
        SELECT p.id_producto, p.name, p.price, p.description, COALESCE(SUM(i.quantity),0) AS stock, c.name AS category
        FROM productos p
        LEFT JOIN inventarios i ON p.id_producto = i.product_id
        INNER JOIN categorias c ON p.category_id = c.id_categoria
        WHERE p.id_producto = :id
        GROUP BY p.id_producto, p.name, p.price, p.description, c.name
    """

    cursor.execute(query, {"id": id_producto})
    productos = cursor.fetchone() #fetchone() para obtener un solo registro

    return {
        "id": productos[0],
        "name": productos[1],
        "price": productos[2],
        "description": productos[3],
        "stock": productos[4],
        "category": productos[5]
    }