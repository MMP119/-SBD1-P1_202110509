from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import cx_Oracle
from database import get_db_connection  



router = APIRouter()



class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    sku: str
    slug: str
    active: str
    stock: int
    location: int
    category: str

@router.post("/products")
def create_product(product: ProductCreate, db=Depends(get_db_connection)):
    cursor = db.cursor()
    
    #obtener el category_id de la categoria
    cursor.execute("SELECT id_categoria FROM categorias WHERE name = :category", {"category": product.category})
    category = cursor.fetchone()
    if not category:
        raise HTTPException(status_code=400, detail="Categoría no válida")
    category_id = category[0]

    # insertar nuevo producto
    insert_product = """
        INSERT INTO productos (category_id, sku, name, description, price, slug, active)
        VALUES (:category_id, :sku, :name, :description, :price, :slug, :active)
        RETURNING id_producto INTO :product_id
    """

    product_id = cursor.var(cx_Oracle.NUMBER)  #variable para capturar el id generado
    cursor.execute(insert_product, {
        "category_id": category_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "sku": product.sku,
        "slug": product.slug,
        "active": product.active,
        "product_id": product_id
    })
    new_product_id = int(product_id.getvalue()[0]) #toma solo el primer valor

    #insertar el stock y locations en inventarios
    insert_inventory = """
        INSERT INTO inventarios (product_id, location_id, quantity)
        VALUES (:product_id, :location, :stock)
    """
    cursor.execute(insert_inventory, {"product_id": new_product_id, "location":product.location ,"stock": product.stock})
    db.commit()

    return {
        "status": 200,
        "message": "Product created successfully",
        "productId": new_product_id
    }
