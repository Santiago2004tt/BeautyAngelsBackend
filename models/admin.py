from db.queries import obtener_tintes_admin, obtener_agendamiento_detallado,actualizar_agendamientos_expirados,cambiar_estado_agendamiento,modificar_cantidad_tinte, obtener_agendamiento_por_nombre,obtener_agendamientos, obtener_agendamientos_pendiente
from fastapi import HTTPException

def get_tintes_admin():
    try:
        tintes = obtener_tintes_admin()
        return {"tintes": tintes}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

def modificar_cantidad_tinte_admin(tinte_id: str, nueva_cantidad: int):
    try:
        modificar_cantidad_tinte(tinte_id, nueva_cantidad)
        return {"message": "Cantidad de tinte modificada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def get_agendamientos_admin():
    try:
        agendamientos = obtener_agendamientos()
        return {"agendamientos": agendamientos}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_agendamientos_pendiente_admin():
    try:
        agendamientos = obtener_agendamientos_pendiente()
        return {"agendamientos": agendamientos}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def get_agendamiento_por_nombre_admin(nombre: str):
    try:
        agendamiento = obtener_agendamiento_por_nombre(nombre)
        return {"agendamiento": agendamiento}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
def cambiar_estado_agendamiento_admin(agendamiento_id: str, nuevo_estado: str):
    try:
        cambiar_estado_agendamiento(agendamiento_id, nuevo_estado)
        return {"message": "Estado del agendamiento modificado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def actualizar_agendamientos_expirados_admin():
    try:
        actualizar_agendamientos_expirados()
        return {"message": "Agendamientos expirados actualizados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def obtener_agendamiento_detallado_admin(agendamiento_id: str):
    try:
        agendamiento = obtener_agendamiento_detallado(agendamiento_id)
        
        return {"agendamiento": agendamiento}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))