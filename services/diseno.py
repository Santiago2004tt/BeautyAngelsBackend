from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import jwt
from jwt import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from db.queries import obtener_disenos, obtener_disenos_por_id
import os

router = APIRouter(prefix="/diseno", tags=["diseno"])

@router.get("/get_disenos")
async def get_disenos():
    try:
        disenos = obtener_disenos()
        return {"disenos": disenos}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/get_diseno/{diseno_id}")
async def get_diseno(diseno_id):
    try:
        disenos = obtener_disenos_por_id(diseno_id)
        return {"diseno": disenos}
        raise HTTPException(status_code=404, detail="Diseño no encontrado")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))