from pydantic import BaseModel, EmailStr

class Cliente(BaseModel):
    id_cliente: int
    id_nacional: int
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str
    contrasena: str
    activo: bool
    correo_confirmado: bool
    created_at: str
    updated_at: str

class CreateClienteRequest(BaseModel):
    id_nacional: int
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str
    contrasena: str
