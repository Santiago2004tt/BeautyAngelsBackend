from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import jwt
from jwt import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from models.user import obtener_nombre_usuario, generar_codigo_verificacion, verificar_codigo, obtener_datos_usuario, obtener_agendamientos
from exception.user_exception import UsuarioError
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

@router.post("/generar_codigo_verificacion/{id_auth}")
async def generar_codigo_verificacion_service(id_auth: str):
    if not id_auth:
        raise HTTPException(status_code=400, detail="El campo 'id_auth' es requerido.")

    try:
        generar_codigo_verificacion(id_auth)
        return {"mensaje": "Código de verificación enviado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el código: {str(e)}")

    

@router.post("/verificar_codigo/{id_auth}")
async def verificar_codigo_service(id_auth: str, request: Request):
    """
    Verifica si el código ingresado por el usuario es correcto.
    """
    try:
        data = await request.json()
        codigo = data.get("codigo")

        if not id_auth or not codigo:
            raise HTTPException(
                status_code=400,
                detail="Los campos 'id_auth' y 'codigo' son requeridos."
            )

        # Lógica de verificación (función ya existente)
        verificar_codigo(id_auth, codigo)

        return {"mensaje": "✅ Código de verificación correcto."}

    except UsuarioError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    
@router.get("/obtener_datos_usuario/{id_auth}")
async def obtener_datos_usuario_endpoint(id_auth: str):
    """
    Endpoint para obtener los datos completos de un usuario a partir del id_auth.
    Se envía directamente en la URL:
    GET /usuario/obtener_datos_usuario/{id_auth}
    """
    try:
        if not id_auth.strip():
            raise HTTPException(status_code=400, detail="El parámetro 'id_auth' es requerido.")

        datos = obtener_datos_usuario(id_auth)

        return {
            "mensaje": "Datos del usuario obtenidos correctamente.",
            "datos_usuario": datos
        }

    except UsuarioError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

    
@router.get("/obtener_agendamientos/{id_auth}")
async def obtener_agendamientos_endpoint(id_auth: str):
    """
    Endpoint para obtener todos los agendamientos de un usuario a partir del id_auth.
    Se envía el id_auth directamente en la URL.
    Ejemplo: GET /usuario/obtener_agendamientos/{id_auth}
    """
    try:
        if not id_auth.strip():
            raise HTTPException(
                status_code=400,
                detail="El parámetro 'id_auth' es requerido."
            )

        agendamientos = obtener_agendamientos(id_auth)

        if not agendamientos or len(agendamientos) == 0:
            return {
                "mensaje": "No se encontraron agendamientos para este usuario.",
                "agendamientos": []
            }

        return {
            "mensaje": "Agendamientos obtenidos correctamente.",
            "agendamientos": agendamientos
        }

    except UsuarioError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )

