from http.client import HTTPException
import supabase
from supabase import create_client, Client
from db.connection import conectar_db
import uuid
from dotenv import load_dotenv
from sqlalchemy import text
import os

def crear_tinte(nombre: str, descripcion: str, imagen: str):
    conn = conectar_db()
    cur = conn.cursor()

    print(cur)

    # Datos de ejemplo para tabla tintes
    id_tinte = str(uuid.uuid4())  # Generar un UUID


    # 2. Insertar en tabla tintes
    cur.execute("""
        INSERT INTO tintes (id, nombre, descripcion, imagen)
        VALUES (%s, %s, %s, %s)
        RETURNING id, nombre, descripcion, imagen;
    """, (id_tinte, nombre, descripcion, imagen))

    nuevo_tinte = cur.fetchone()
    conn.commit()

    print("✅ Tinte insertado:", nuevo_tinte)

    cur.close()
    conn.close()


def registrar_usuario(email: str, password: str, nombre: str,telefono: str, rol: str):
    # Cliente de Supabase (Auth)
    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    conn = conectar_db()
    cur = conn.cursor()

    resp = supabase.auth.sign_up({
    "email": email,
    "password": password
    })
    auth_id = resp.user.id
    cur.execute("""
        INSERT INTO usuarios (auth_id, nombre, telefono, rol)
        VALUES (%s, %s, %s, %s)
        RETURNING id, creado_en;
    """, (auth_id, nombre, telefono, rol))

    conn.commit()

    cur.close()
    conn.close()


def iniciar_sesion(email: str, password: str):
    load_dotenv()
    # Cargar credenciales del proyecto
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # 🔑 Usa la "anon key" para login de usuarios
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Intentar login
    resp = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if resp.session is None:
        raise Exception("Error al iniciar sesión: credenciales inválidas o cuenta no confirmada.")

    # Extraer datos importantes
    access_token = resp.session.access_token
    refresh_token = resp.session.refresh_token
    user_info = resp.user

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user_info.id,
            "email": user_info.email
        }
    }

def obtener_nombre_usuario(id: str):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT nombre FROM usuarios WHERE auth_id = %s;
    """, (id,))
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    if resultado:
        return resultado[0]  # Retorna el nombre
    else:
        raise Exception("Usuario no encontrado.")
    
def obtener_id_usuario(id: str):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id FROM usuarios WHERE auth_id = %s;
    """, (id,))
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    if resultado:
        return resultado[0]  # Retorna el nombre
    else:
        raise Exception("Usuario no encontrado.")

def obtener_disenos():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, descripcion, imagen FROM disenos;
    """)
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    disenios = []
    for fila in resultados:
        disenio = {
            "id": fila[0],
            "nombre": fila[1],
            "descripcion": fila[2],
            "imagen": fila[3]
        }
        disenios.append(disenio)
    return disenios

def obtener_disenos_por_id(disenio_id: str):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, descripcion, imagen, max_tintes,precio_estimado FROM disenos WHERE id = %s;
    """, (disenio_id,))
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    if resultado:
        disenio = {
            "id": resultado[0],
            "nombre": resultado[1],
            "descripcion": resultado[2],
            "imagen": resultado[3],
            "max_tintes":resultado[4],
            "precio_estimado":resultado[5]
        }
        return disenio
    else:
        raise Exception("Diseño no encontrado.")


def obtener_horarios_ocupados(fecha: str):
    """
    Devuelve lista de horas ocupadas en formato 'HH:MM' para la fecha indicada.
    """
    try:
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT hora 
            FROM agendamientos 
            WHERE fecha = %s;
        """, (fecha,))
        resultados = cur.fetchall()
        cur.close()
        conn.close()

        horas = []
        for r in resultados:
            valor = r[0]
            if hasattr(valor, "strftime"):  # tipo datetime.time
                horas.append(valor.strftime("%H:%M"))
            elif isinstance(valor, str):  # tipo texto en DB
                horas.append(valor[:5])  # "HH:MM:SS" → "HH:MM"
        return horas

    except Exception as e:
        print("Error al obtener horarios ocupados:", e)
        return []



def obtener_tintes():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, descripcion, imagen FROM tintes;
    """)
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    tintes = []
    for fila in resultados:
        tinte = {
            "id": fila[0],
            "nombre": fila[1],
            "descripcion": fila[2],
            "imagen": fila[3]
        }
        tintes.append(tinte)
    return tintes

def crear_agendamiento(usuario_id, diseno_id, fecha, hora, estado="pendiente"):
    try:
        conn = conectar_db()
        cur = conn.cursor()

        query = """
            INSERT INTO agendamientos (usuario_id, diseno_id, fecha, hora, estado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """
        cur.execute(query, (usuario_id, diseno_id, fecha, hora, estado))
        nuevo_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return nuevo_id
    except Exception as e:
        print("Error al crear agendamiento:", e)
        return None
    
def crear_agendamiento_con_tintes(usuario_id, diseno_id, fecha, hora, tintes_ids: list, estado="pendiente"):
    try:
        conn = conectar_db()
        cur = conn.cursor()

        # 1. Crear agendamiento
        query_agendamiento = """
            INSERT INTO agendamientos (usuario_id, diseno_id, fecha, hora, estado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """
        cur.execute(query_agendamiento, (usuario_id, diseno_id, fecha, hora, estado))
        nuevo_agendamiento_id = cur.fetchone()[0]

        # 2. Asociar tintes si hay
        if tintes_ids:
            query_tintes = """
                INSERT INTO agendamiento_tinte (agendamiento_id, tinte_id)
                VALUES (%s, %s);
            """
            for tinte_id in tintes_ids:
                cur.execute(query_tintes, (nuevo_agendamiento_id, tinte_id))

        conn.commit()
        cur.close()
        conn.close()

        return nuevo_agendamiento_id
    except Exception as e:
        print("Error al crear agendamiento con tintes:", e)
        return None