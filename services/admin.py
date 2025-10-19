from fastapi import APIRouter, HTTPException
from models.admin import get_tintes_admin,obtener_agendamiento_detallado_admin,cambiar_estado_agendamiento_admin,get_agendamiento_por_nombre_admin ,modificar_cantidad_tinte_admin,get_agendamientos_admin, get_agendamientos_pendiente_admin, actualizar_agendamientos_expirados_admin
router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/get_tintes_admin")
async def tintes_admin():
    return get_tintes_admin()

@router.post("/modificar_cantidad_tinte/{tinte_id}/{nueva_cantidad}")
async def modificar_cantidad_tinte(tinte_id: str, nueva_cantidad: int):
    return modificar_cantidad_tinte_admin(tinte_id, nueva_cantidad)

@router.get("/get_agendamientos_admin")
async def agendamientos_admin():

    return get_agendamientos_admin()

@router.get("/get_agendamientos_pendiente_admin")
async def agendamientos_admin():

    return get_agendamientos_pendiente_admin()

@router.get("/get_agendamiento_por_nombre_admin/{nombre}")
async def agendamiento_por_nombre_admin(nombre: str):
    return get_agendamiento_por_nombre_admin(nombre)

@router.post("/cambiar_estado_agendamiento_admin/{agendamiento_id}/{nuevo_estado}")
async def cambiar_estado_agendamiento(agendamiento_id: str, nuevo_estado: str):
    return cambiar_estado_agendamiento_admin(agendamiento_id, nuevo_estado)

@router.post("/actualizar_agendamientos_expirados_admin")
async def actualizar_agendamientos_expirados():
    return actualizar_agendamientos_expirados_admin()

@router.get("/obtener_agendamiento_detallado_admin/{agendamiento_id}")
async def obtener_agendamiento_detallado(agendamiento_id: str):
    
    return obtener_agendamiento_detallado_admin(agendamiento_id)