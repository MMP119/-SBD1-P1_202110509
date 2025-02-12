from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse
from typing import Dict


router = APIRouter() # sirve para definir rutas


@router.post("/patments")  # REGISTRA UN PAGO ASOCIADO A UNA ORDEM
async def register_payment(request: Request):
    return JSONResponse(content={"status":"success", "message": "Payment registered successfully"}, status_code=200)



@router.get("/payments")  # Lista los pagos realizados, con posibilidad de filtrar por orden, fecha, método, etc.
async def get_payments():
    return JSONResponse(content={"status":"success", "message": "Payments retrieved successfully"}, status_code=200)