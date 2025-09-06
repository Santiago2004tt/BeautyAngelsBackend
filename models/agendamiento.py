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


def obtener_horas_disponibles(fecha: str):
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        if fecha_obj < datetime.now().date():
            raise HTTPException(status_code=400, detail="Fecha no válida (ya pasó)")

        horas_base = [f"{h:02d}:00" for h in range(8, 21)]
        horas_ocupadas = obtener_horarios_ocupados(fecha)  # lista de strings ["10:00", "15:00"]

        horas_bloqueadas = set()
        for hora in horas_ocupadas:
            ag_inicio = datetime.strptime(hora, "%H:%M")
            for delta in range(-2, 3):
                bloqueada = (ag_inicio + timedelta(hours=delta)).strftime("%H:%M")
                horas_bloqueadas.add(bloqueada)

        horas_validas = [h for h in horas_base if h not in horas_bloqueadas]

        return {"fecha": fecha, "horas": horas_validas}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")