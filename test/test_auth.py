import os
from supabase import create_client, Client
from dotenv import load_dotenv
from models.user import iniciar_sesion




def test_validate():
    # Ejemplo de uso
    if __name__ == "__main__":
        email = "santiagosepulvedabran@gmail.com"
        password = "Password1*"

        sesion = iniciar_sesion(email, password)
        print("✅ Sesión iniciada:")
        print("Token:", sesion["access_token"])
        print("Usuario:", sesion["user"])
        print("Token de actualización:", sesion["refresh_token"])

test_validate()