from fastapi import APIRouter, HTTPException, Body, Path, Depends
from pydantic import BaseModel
from database import get_db_connection
from datetime import datetime

router = APIRouter()

# Modelo para actualizar productos (campos opcionales)
class ProductUpdate(BaseModel):
    category_id: int = None
    sku: str = None
    name: str = None
    description: str = None
    price: float = None
    slug: str = None
    active: str = None

@router.put("/products/:{product_id}")
def update_product(
    product_id: int = Path(..., title="ID del producto", ge=1), #ge=1 es para que el id sea mayor o igual a 1
    product_data: dict = Body(...),
    db=Depends(get_db_connection)
    ):
    
    cursor = db.cursor()

    # Verificar si el producto existe
    cursor.execute("SELECT id_producto FROM productos WHERE id_producto = :product_id", {"product_id": product_id})
    existing_product = cursor.fetchone()
    
    if not existing_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    

    # Componer la consulta de actualización
    set_clause = ", ".join([f"{key} = :{key}" for key in product_data.keys()])
    product_data["updated_at"] = datetime.now()

    update_query = f"""
        UPDATE productos
        SET {set_clause}, updated_at = :updated_at
        WHERE id_producto = :product_id
    """

    product_data["product_id"] = product_id
    cursor.execute(update_query, product_data)
    db.commit()


    return {
        "status": 200,
        "message": "Product updated successfully"
    }
