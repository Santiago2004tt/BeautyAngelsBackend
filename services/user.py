from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import jwt
from jwt import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from models.user import obtener_nombre_usuario
import os

router = APIRouter(prefix="/user", tags=["user"])

class userName(BaseModel):
    user_id: str
    
@router.get("/get_user_name/{user_id}")
async def get_user_name(user_id: str):
    try:
        nombre = obtener_nombre_usuario(user_id)
        return {"nombre": nombre}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
