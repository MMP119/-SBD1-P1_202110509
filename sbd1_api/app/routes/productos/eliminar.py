from fastapi import APIRouter, HTTPException, Path, Depends
from database import get_db_connection

router = APIRouter()

@router.delete("/products/:{product_id}")
def delete_product(product_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor()
    
    # Verificar si el producto existe
    cursor.execute("SELECT * FROM productos WHERE id_producto = :product_id", {"product_id": product_id})
    product = cursor.fetchone()

    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    #se elimina 
    cursor.execute("DELETE FROM productos WHERE id_producto = :product_id", {"product_id": product_id})
    db.commit()

    return {
        "status": 200,
        "message": "Product deleted successfully"
    }
