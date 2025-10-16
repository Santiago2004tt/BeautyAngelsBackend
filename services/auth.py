from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.user import crear_usuario, iniciar_sesion, obtener_rol_correo

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
    

@router.post("/login_admin")
async def login_admin(user: UserLogin):
    try:
        rol = obtener_rol_correo(user.email)
        print(rol)
        if(rol != "admin"):
            raise HTTPException(status_code=403, detail="Acceso denegado: No es un usuario administrador")
        sesion = iniciar_sesion(user.email, user.password)
        return {"message": "Sesión de administrador iniciada exitosamente", "session": sesion}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
