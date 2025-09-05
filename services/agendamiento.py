from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import jwt
from jwt import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import List
from db.queries import obtener_horarios_ocupados
import os

router = APIRouter(prefix="/agendamiento", tags=["agendamiento"])



@router.get("/horas_disponibles")
async def horas_disponibles(fecha: str):
    try:
        # Validar formato de fecha
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido (YYYY-MM-DD)")

        if fecha_obj < datetime.now().date():
            raise HTTPException(status_code=400, detail="Fecha no válida (ya pasó)")

        # Generar todas las horas base entre 08:00 y 20:00
        horas_base = [f"{h:02d}:00" for h in range(8, 21)]

        # Obtener agendamientos de esa fecha desde la BD
        agendamientos = obtener_horarios_ocupados(fecha)
        # Ejemplo esperado: [{"inicio": "10:00"}, {"inicio": "15:00"}]

        # Construir lista de horas ocupadas (con rango ±2h)
        horas_bloqueadas = set()
        for ag in agendamientos:
            ag_inicio = datetime.strptime(ag["inicio"], "%H:%M")
            for delta in range(-2, 2):  # -2h, -1h, 0h, +1h, +2h
                bloqueada = (ag_inicio + timedelta(hours=delta)).strftime("%H:%M")
                horas_bloqueadas.add(bloqueada)

        # Filtrar horas válidas
        horas_validas = [h for h in horas_base if h not in horas_bloqueadas]

        return {"fecha": fecha, "horas": horas_validas}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")