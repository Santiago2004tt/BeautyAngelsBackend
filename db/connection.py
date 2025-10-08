import os
from dotenv import load_dotenv
import psycopg2


### Conexión a la base de datos
def conectar_db():
    # 1) Cargar variables
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    
    if not url:
        raise ValueError("La variable de entorno DATABASE_URL no está definida.")
    
    conn= psycopg2.connect(url, sslmode="require")
    return conn


