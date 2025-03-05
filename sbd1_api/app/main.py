from fastapi import FastAPI

#enpoints de clientes
from routes.clientes.clientes import router as clientes_router
from routes.clientes.autenticacion import router as cliente_autenticacion_router
from routes.clientes.obtenerDatosEsp import router as cliente_obtenerDatosEsp_router
from routes.clientes.actualizar import router as cliente_actualizar_router
from routes.clientes.eliminar import router as cliente_eliminar_router

#endpoints de productos
from routes.productos.listar import router as listar_productos_router
from routes.productos.detalle import router as detalle_productos_router
from routes.productos.crear import router as crear_productos_router
from routes.productos.actualizar import router as actualizar_productos_router
from routes.productos.eliminar import router as eliminar_productos_router


#enpoints de ordenes
from routes.ordenes.crear import router as crear_ordenes_router
from routes.ordenes.listar import router as listar_ordenes_router
from routes.ordenes.detalle import router as detalle_ordenes_router
from routes.ordenes.actualizar import router as actualizar_ordenes_router


app = FastAPI()


app.include_router(clientes_router)
app.include_router(cliente_autenticacion_router)
app.include_router(cliente_obtenerDatosEsp_router)
app.include_router(cliente_actualizar_router)
app.include_router(cliente_eliminar_router)
app.include_router(listar_productos_router)
app.include_router(detalle_productos_router)
app.include_router(crear_productos_router)
app.include_router(actualizar_productos_router)
app.include_router(eliminar_productos_router)
app.include_router(crear_ordenes_router)
app.include_router(listar_ordenes_router)
app.include_router(detalle_ordenes_router)
app.include_router(actualizar_ordenes_router)



@app.get("/")
def read_root():
    return {"message": "API con Oracle funcionando"}
