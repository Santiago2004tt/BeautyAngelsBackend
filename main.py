from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import auth, user, diseno, agendamiento, admin

app = FastAPI()

# 🟢 Agrega todos los orígenes posibles
origins = [
    "http://localhost:3000",                # React local
    "http://127.0.0.1:3000",                # Alternativo local
    "https://beauty-angels-frontend.vercel.app",  # Tu frontend desplegado
    "https://beautyangelsbackend.onrender.com"    # Backend render (para preflight correcto)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(diseno.router)
app.include_router(agendamiento.router)
app.include_router(admin.router)
