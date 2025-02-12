from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse
from typing import Dict


router = APIRouter() # sirve para definir rutas



@router.get("/products")  # RETORNA LA LISTA DE PRODUCTOS
async def get_products():
    return JSONResponse(content={"status":"success", "message": "Products retrieved successfully"}, status_code=200)




@router.get("/products/:{id}")  # RETORNA UN PRODUCTO ESPECÍFICO, SOLO LOS DETALLES
async def get_details_product(id: int):
    return JSONResponse(content={"status":"success", "message": "Product retrieved successfully"}, status_code=200)




@router.post("/products", status_code=201)  # CREAR UN NUEVO PRODUCTO 
async def create_product(request: Request):
    
    #terminar una vez se tenga acceso a la base de datos
    return JSONResponse(content={"status":"success", "message": "Product created successfully"}, status_code=201)




@router.put("/products/:{id}", status_code=200)  # ACTUALIZAR UN PRODUCTO
async def update_product(id: int, request: Request):
    
    #terminar una vez se tenga acceso a la base de datos
    return JSONResponse(content={"status":"success", "message": "Product updated successfully"}, status_code=200)




@router.delete("/products/:{id}", status_code=200)  # ELIMINAR UN PRODUCTO
async def delete_product(id: int):
        
    #terminar una vez se tenga acceso a la base de datos
    return JSONResponse(content={"status":"success", "message": "Product deleted successfully"}, status_code=200)