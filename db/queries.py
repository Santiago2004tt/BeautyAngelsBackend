from http.client import HTTPException
import supabase
from supabase import create_client, Client
from db.connection import conectar_db
import uuid
from dotenv import load_dotenv
from sqlalchemy import text
import os


# Funciones para interactuar con la base de datos
# Crear un nuevo tinte
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

# Registrar un nuevo usuario
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

# Iniciar sesión
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

# Obtener nombre de usuario por auth_id
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

# Obtener id de usuario por auth_id   
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

# Obtener todos los diseños
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

# Obtener diseño por id
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


# Obtener horarios ocupados para una fecha
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


# Obtener todos los tintes
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

# Crear un nuevo agendamiento
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

# Crear un nuevo agendamiento con tintes opcionales 
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

        # 2. Asociar tintes y actualizar cantidad
        if tintes_ids:
            query_tintes = """
                INSERT INTO agendamiento_tinte (agendamiento_id, tinte_id)
                VALUES (%s, %s);
            """
            query_restar_cant = """
                UPDATE tintes
                SET cant = GREATEST(cant - 1, 0)
                WHERE id = %s;
            """

            for tinte_id in tintes_ids:
                cur.execute(query_tintes, (nuevo_agendamiento_id, tinte_id))
                cur.execute(query_restar_cant, (tinte_id,))

        conn.commit()
        cur.close()
        conn.close()

        return nuevo_agendamiento_id

    except Exception as e:
        print("❌ Error al crear agendamiento con tintes:", e)
        return None

    
# Obtener fechas y horas de agendamientos por auth_user_id
def obtener_fechas_horas_por_auth_id(auth_user_id: str):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT ag.fecha, ag.hora
        FROM agendamientos ag
        JOIN usuarios u ON u.id = ag.usuario_id
        JOIN auth.users us ON u.auth_id = us.id
        WHERE us.id = %s
        ORDER BY ag.fecha DESC, ag.hora DESC;
    """, (auth_user_id,))
    
    resultados = cur.fetchall()
    cur.close()
    conn.close()

    agendamientos = []
    for fila in resultados:
        agendamiento = {
            "fecha": fila[0].strftime("%Y-%m-%d"),
            "hora": fila[1].strftime("%H:%M")
        }
        agendamientos.append(agendamiento)

    return agendamientos

# Guardar código de verificación para un usuario
def guardar_codigo_verificacion(id_usuario: str, codigo: str):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE usuarios
        SET codigo_ver = %s
        WHERE id = %s
        RETURNING id;
    """, (codigo, id_usuario))
    actualizado_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return actualizado_id

# Obtener correo del usuario a partir del id_usuario
def obtener_correo_usuario(id_usuario: str):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT au.email
        FROM auth.users au
        JOIN usuarios u ON u.auth_id = au.id
        WHERE u.id = %s;
    """, (id_usuario,))
    
    resultado = cur.fetchone()
    cur.close()
    conn.close()

    if resultado:
        return resultado[0]  # Retorna el correo real
    else:
        return None
    
# Obtener código de verificación por id_usuario  
def obtener_codigo_verificacion(id_usuario: str):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT codigo_ver
        FROM usuarios
        WHERE id = %s;
    """, (id_usuario,))
    resultado = cur.fetchone()
    cur.close()
    conn.close()

    if resultado:
        return resultado[0]  # Retorna el codigo de verificación
    else:
        return None
    
#Obtener datos de usuario por id
def obtener_datos_usuario_por_id(id_usuario: str):

    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, telefono, rol, creado_en
        FROM usuarios
        WHERE id = %s;
    """, (id_usuario,))
    resultado = cur.fetchone()
    cur.close()
    conn.close()

    if resultado:
        usuario = {
            "id": resultado[0],
            "nombre": resultado[1],
            "telefono": resultado[2],
            "rol": resultado[3],
            "creado_en": resultado[4].strftime("%Y-%m-%d %H:%M:%S"),
            "correo": obtener_correo_usuario(resultado[0])
        }
        return usuario
    else:
        return None
    

#  Obtener todos los agendamientos de un usuario por su usuario_id
def obtener_agendamientos_por_usuario_id(usuario_id: str):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            id,
            usuario_id,
            diseno_id,
            fecha,
            hora,
            estado,
            creado_en
        FROM agendamientos
        WHERE usuario_id = %s
        ORDER BY fecha DESC, hora DESC;
    """, (usuario_id,))
    
    resultados = cur.fetchall()
    cur.close()
    conn.close()

    agendamientos = []
    for fila in resultados:
        agendamiento = {
            "id": str(fila[0]),
            "usuario_id": str(fila[1]) if fila[1] else None,
            "diseno_id": str(fila[2]) if fila[2] else None,
            "fecha": fila[3].strftime("%Y-%m-%d") if fila[3] else None,
            "hora": fila[4].strftime("%H:%M") if fila[4] else None,
            "estado": fila[5],
            "creado_en": fila[6].strftime("%Y-%m-%d %H:%M:%S") if fila[6] else None
        }
        agendamientos.append(agendamiento)

    return agendamientos

# Obtener rol del usuario a partir del correo
def obtener_rol_correo_query(correo: str):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.rol
        FROM usuarios u
        JOIN auth.users au ON u.auth_id = au.id
        WHERE au.email = %s;
    """, (correo,))
    
    resultado = cur.fetchone()
    cur.close()
    conn.close()

    if resultado:
        return resultado[0]  # Retorna el rol
    else:
        return None