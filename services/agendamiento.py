from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import jwt
from jwt import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import List
from models.agendamiento import obtener_horas_disponibles, agendar
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