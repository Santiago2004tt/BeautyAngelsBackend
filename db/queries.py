from http.client import HTTPException
import supabase
from supabase import create_client, Client
from supabase_auth import datetime
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


# Obtener todos los tintes para el usuario
def obtener_tintes():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, descripcion, imagen 
        FROM tintes
        WHERE cant > 3;
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

# Obtener todos los tintes para el usuario
def obtener_tintes_admin():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, descripcion, imagen, cant
        FROM tintes;
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
            "imagen": fila[3],
            "cant": fila[4]
        }
        tintes.append(tinte)
    return tintes

#Modificar cantidad de tinte usando la variable cant 
def modificar_cantidad_tinte(tinte_id: int, cantidad: int):
    """
    Modifica la cantidad (cant) de un tinte sumando o restando el valor indicado.
    Si el resultado es menor que 0, la cantidad se deja en 0.
    Retorna el nuevo valor de 'cant' o None si ocurre un error.
    """
    try:
        conn = conectar_db()
        cur = conn.cursor()

        # Obtener cantidad actual
        cur.execute("SELECT cant FROM tintes WHERE id = %s;", (tinte_id,))
        resultado = cur.fetchone()

        if not resultado:
            print("❌ No se encontró el tinte con ese ID.")
            return None

        cant_actual = resultado[0]
        nueva_cant = cant_actual + cantidad

        # Evitar cantidades negativas
        if nueva_cant < 0:
            nueva_cant = 0

        # Actualizar en base de datos
        cur.execute(
            """
            UPDATE tintes
            SET cant = %s
            WHERE id = %s
            RETURNING cant;
            """,
            (nueva_cant, tinte_id)
        )

        nueva_cant_db = cur.fetchone()[0]
        conn.commit()

        print(f"✅ Cantidad actualizada correctamente. Nueva cantidad: {nueva_cant_db}")
        return nueva_cant_db

    except Exception as e:
        print("❌ Error al modificar cantidad de tinte:", e)
        return None

    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()

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

#Metodo para cancelar agendamiento
def cancelar_agendamiento(agendamiento_id: str):
    try:
        conn = conectar_db()
        cur = conn.cursor()

        query = """
            UPDATE agendamientos
            SET estado = 'cancelado'
            WHERE id = %s
            RETURNING id;
        """
        cur.execute(query, (agendamiento_id,))
        actualizado_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return actualizado_id
    except Exception as e:
        print("Error al cancelar agendamiento:", e)
        return None
    
#Metodo para obtener todos los agendamientos pendientes del (admin)
def obtener_agendamientos_pendiente():
    try:
        conn = conectar_db()
        cur = conn.cursor()

        query = """
            SELECT id, usuario_id, diseno_id, fecha, hora, estado, creado_en
            FROM agendamientos
            WHERE estado = 'pendiente'
            ORDER BY fecha DESC, hora DESC;
        """
        cur.execute(query)
        resultados = cur.fetchall()

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

        cur.close()
        conn.close()

        return agendamientos

    except Exception as e:
        print("Error al obtener agendamientos:", e)

#Metodo para obtener todos los agendamientos (admin)
def obtener_agendamientos():
    try:
        conn = conectar_db()
        cur = conn.cursor()

        query = """
            SELECT id, usuario_id, diseno_id, fecha, hora, estado, creado_en
            FROM agendamientos
            ORDER BY fecha DESC, hora DESC;
        """
        cur.execute(query)
        resultados = cur.fetchall()

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

        cur.close()
        conn.close()

        return agendamientos

    except Exception as e:
        print("Error al obtener agendamientos:", e)

#Buscar agendamiento por nombre de usuario
def obtener_agendamiento_por_nombre(nombre: str):
    try:
        conn = conectar_db()
        cur = conn.cursor()

        query = """
            SELECT ag.id, ag.usuario_id, ag.diseno_id, ag.fecha, ag.hora, ag.estado, ag.creado_en
            FROM agendamientos ag
            JOIN usuarios u ON ag.usuario_id = u.id
            WHERE u.nombre ILIKE %s
            ORDER BY ag.fecha DESC, ag.hora DESC;
        """
        cur.execute(query, (f"%{nombre}%",))
        resultados = cur.fetchall()

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

        cur.close()
        conn.close()

        return agendamientos

    except Exception as e:
        print("Error al obtener agendamientos por nombre:", e)
        return []
    

def cambiar_estado_agendamiento(agendamiento_id: str, nuevo_estado: str):
    try:
        conn = conectar_db()
        cur = conn.cursor()

        query = """
            UPDATE agendamientos
            SET estado = %s
            WHERE id = %s
            RETURNING id, estado;
        """
        cur.execute(query, (nuevo_estado, agendamiento_id))
        resultado = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if resultado:
            return {
                "id": str(resultado[0]),
                "estado": resultado[1]
            }
        else:
            return None

    except Exception as e:
        print("Error al cambiar estado de agendamiento:", e)
        return None
    
def actualizar_agendamientos_expirados():
    try:
        conn = conectar_db()
        cur = conn.cursor()

        # Obtenemos la fecha y hora actual
        ahora = datetime.now()

        # Actualizamos todos los agendamientos que ya pasaron
        query = """
            UPDATE agendamientos
            SET estado = 'expiro'
            WHERE (fecha + hora) < %s
              AND estado NOT IN ('cancelado', 'expiro')
            RETURNING id, fecha, hora;
        """
        cur.execute(query, (ahora,))
        resultados = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()

        # Retorna los IDs actualizados
        if resultados:
            return [
                {"id": str(f[0]), "fecha": str(f[1]), "hora": str(f[2])}
                for f in resultados
            ]
        else:
            return []

    except Exception as e:
        print("Error al actualizar agendamientos expirados:", e)
        return None

#Obtener agendamiento detallado por id (admin)
def obtener_agendamiento_detallado(agendamiento_id: str):
    """
    Obtiene la información detallada de un agendamiento con la lista completa de tintes asociados.
    """
    try:
        conn = conectar_db()
        cur = conn.cursor()

        query = """
            SELECT 
                u.nombre AS usuario_nombre,
                ag.fecha,
                ag.hora,
                ag.estado,
                d.descripcion AS diseno_descripcion,
                t.id AS tinte_id,
                t.nombre AS tinte_nombre,
                t.imagen AS tinte_imagen,
                d.precio_estimado
            FROM agendamientos ag
            JOIN usuarios u ON u.id = ag.usuario_id
            JOIN disenos d ON d.id = ag.diseno_id
            JOIN agendamiento_tinte at ON at.agendamiento_id = ag.id
            JOIN tintes t ON t.id = at.tinte_id
            WHERE ag.id = %s;
        """

        cur.execute(query, (agendamiento_id,))
        filas = cur.fetchall()

        cur.close()
        conn.close()

        if not filas:
            return None

        # Tomamos los datos comunes de la primera fila
        primera = filas[0]
        agendamiento = {
            "usuario_nombre": primera[0],
            "fecha": primera[1].strftime("%Y-%m-%d") if primera[1] else None,
            "hora": primera[2].strftime("%H:%M") if primera[2] else None,
            "estado": primera[3],
            "diseno_descripcion": primera[4],
            "tintes": [],
            "precio_estimado": float(primera[8]) if primera[8] is not None else None
        }

        # Recorremos todas las filas y acumulamos los tintes
        for f in filas:
            tinte = {
                "id": str(f[5]) if f[5] is not None else None,
                "nombre": f[6],
                "imagen": f[7]
            }
            agendamiento["tintes"].append(tinte)

        return agendamiento

    except Exception as e:
        print("❌ Error al obtener agendamiento detallado:", e)
        return None