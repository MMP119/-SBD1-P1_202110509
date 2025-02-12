from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse
from typing import Dict

router = APIRouter() # sirve para definir rutas


@router.post("orders", status_code=201)  # CREAR UNA NUEVA ORDEN ASOCIADA A UN USUARIO
async def create_order(request: Request):
    return JSONResponse(content={"status":"success", "message": "Order created successfully"}, status_code=201)




@router.get("/orders")  # Retorna un listado de órdenes. Se pueden añadir filtros (por estado, fecha, etc.).
async def get_orders():
    return JSONResponse(content={"status":"success", "message": "Orders retrieved successfully"}, status_code=200)




@router.get("/orders/:{id}")  # Retorna los detalles de una orden específica, incluyendo items, cantidades etc.
async def get_details_order(id: int):
    return JSONResponse(content={"status":"success", "message": "Order retrieved successfully"}, status_code=200)



@router.put("/orders/:{id}", status_code=200)  # Actualiza una orden específica. PERMITE CAMBIAR SOLO EL ESTADO DE LA ORDEN, processing, shipped, delivered, cancelled
async def update_order(id: int, request: Request):
    return JSONResponse(content={"status":"success", "message": "Order updated successfully"}, status_code=200)

