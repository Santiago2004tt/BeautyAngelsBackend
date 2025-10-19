from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import auth
from services import user
from services import diseno
from services import agendamiento
from services import admin
app = FastAPI()

# Orígenes permitidos
origins = [
    "http://localhost:3000",  # frontend dev
    "http://127.0.0.1:3000",
     "https://beauty-angels-frontend.vercel.app" # otro posible host local
    # puedes poner "*" en desarrollo, pero no en producción
]

# CORS para permitir peticiones desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://beauty-angels-frontend.vercel.app"],  # puerto donde corre tu React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# incluir las rutas
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(diseno.router)
app.include_router(agendamiento.router)
app.include_router(admin.router)