from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import jwt
from jwt import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import List
from models.agendamiento import obtener_horas_disponibles, agendar, obtener_agendamiento_proximo_por_usuario
from db.queries import obtener_id_usuario
import os

router = APIRouter(prefix="/agendamiento", tags=["agendamiento"])

class AgendamientoRequest(BaseModel):
    usuario_id: str
    diseno_id: str
    fecha: str
    hora: str
    tintes_ids: List[str]
    max_tintes: int

@router.get("/horas_disponibles")
async def horas_disponibles(fecha: str):
    return obtener_horas_disponibles(fecha)




@router.post("/crear_agendamiento")
async def crear_agendamiento_endpoint(req: AgendamientoRequest):
    try:
        user_id = obtener_id_usuario(req.usuario_id)

        nuevo_id = agendar(
            user_id,
            req.diseno_id,
            req.fecha,
            req.hora,
            req.tintes_ids,
            req.max_tintes
        )

        return {"status": "success", "agendamiento_id": nuevo_id}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    
@router.post("/agendamiento_proximo")
async def obtener_agendamiento_proximo_service(request: Request):
    """
    Endpoint para obtener el agendamiento más próximo de un usuario.
    Espera un JSON con el campo 'usuario_id'.
    """
    try:
        data = await request.json()
        usuario_id = data.get("usuario_id")

        if not usuario_id:
            raise HTTPException(status_code=400, detail="El campo 'usuario_id' es requerido.")

        agendamiento = obtener_agendamiento_proximo_por_usuario(usuario_id)
        print(agendamiento)

        if agendamiento is None:
            return {"mensaje": "No se encontraron agendamientos futuros para este usuario."}

        return {
            "mensaje": "Agendamiento más próximo encontrado.",
            "agendamiento": agendamiento
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
