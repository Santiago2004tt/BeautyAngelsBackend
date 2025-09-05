from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import jwt
from jwt import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from models.user import crear_usuario, iniciar_sesion
from supabase import create_client, Client
import os

router = APIRouter(prefix="/auth", tags=["auth"])


# Modelos
class UserRegister(BaseModel):
    email: str
    nombre: str
    telefono: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register_user")
async def register_user(user: UserRegister):
    # Lógica para registrar al usuario
    try:
        print(user.email, user.nombre, user.telefono, user.password)
        crear_usuario(user.email, user.nombre, user.telefono, user.password)
        return {"message": "Usuario registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: UserLogin):  
    try:
        sesion = iniciar_sesion(user.email, user.password)
        return {"message": "Sesión iniciada exitosamente", "session": sesion}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
