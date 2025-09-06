from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import jwt
from jwt import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import List
from models.agendamiento import obtener_horas_disponibles
import os

router = APIRouter(prefix="/agendamiento", tags=["agendamiento"])



@router.get("/horas_disponibles")
async def horas_disponibles(fecha: str):
    return obtener_horas_disponibles(fecha)
        