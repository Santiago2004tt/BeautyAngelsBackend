from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import auth
from services import user
from services import diseno
from services import agendamiento
app = FastAPI()

# CORS para permitir peticiones desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # puerto donde corre tu React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# incluir las rutas
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(diseno.router)
app.include_router(agendamiento.router)