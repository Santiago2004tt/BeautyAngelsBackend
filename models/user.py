from exception.user_exception import (
    UsuarioError,
    CorreoInvalido,
    ContraseniaInvalida,
    CampoVacio,
)
from models.user_service import verificar_contrasenia_escrito, verificar_email
from db.queries import registrar_usuario, obtener_datos_usuario_por_id ,iniciar_sesion, obtener_nombre_usuario,guardar_codigo_verificacion,obtener_id_usuario,obtener_correo_usuario, obtener_codigo_verificacion, obtener_agendamientos_por_usuario_id
import smtplib
import random
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart

# Función para crear un nuevo usuario con validaciones
def crear_usuario(correo: str, nombre: str, telefono: str, password: str):


    if (not verificar_email(correo)) :
        raise CorreoInvalido("El correo no cumple con el formato adecuado.")
    if (not verificar_contrasenia_escrito(password)):
        raise ContraseniaInvalida("La contraseña no cumple con los requisitos de seguridad.")
    
    #if buscar si existe el correo en la base de datos:
    #    raise user_exception("El correo ya está registrado.")
    # Validar campos vacíos

    if not nombre or not nombre.strip():
        raise CampoVacio("El campo 'nombre' no puede estar vacío.")
    
    if not telefono or not telefono.strip():
        raise CampoVacio("El campo 'teléfono' no puede estar vacío.")
    
    print("Todos los datos son válidos. Procediendo a registrar el usuario...")
    registrar_usuario(correo, password, nombre, telefono, "cliente")

# Función para iniciar sesión con validaciones
def login_usuario(correo: str, password: str):
    if not correo or not correo.strip():
        raise CampoVacio("El campo 'correo' no puede estar vacío.")
    if not password or not password.strip():
        raise CampoVacio("El campo 'contraseña' no puede estar vacío.") 
    if (not verificar_email(correo)) :
        raise CorreoInvalido("El correo no cumple con el formato adecuado.")
    iniciar_sesion(correo, password)

# Función para obtener el nombre de usuario por ID con validaciones
def obtener_nombre(id: str):
    if not id:
        raise CampoVacio("El campo 'id' no puede estar vacío.")
    else:
        return obtener_nombre_usuario(id)
    

#Generar código de verificación
def generar_codigo_verificacion(id_auth: str):
    id_usuario = obtener_id_usuario(id_auth)
    destinatario = obtener_correo_usuario(id_usuario)
    codigo = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    if(id_usuario == ""):
        raise UsuarioError("El id no puede estar vacío.")
    else:
        guardar_codigo_verificacion(id_usuario, codigo)
        enviar_correo(destinatario, codigo)

#Verificar código de verificación
def verificar_codigo(id_auth: str, codigo: str):
    id_usuario = obtener_id_usuario(id_auth)
    if(id_usuario == ""):
        raise UsuarioError("El id no puede estar vacío.")
    else:
        codigo_almacenado = obtener_codigo_verificacion(id_usuario)

        if codigo_almacenado is None:
            raise UsuarioError("No se encontró un código de verificación para este usuario.")
        if codigo == codigo_almacenado:
            return True
        else:
            
            raise UsuarioError("El código de verificación es incorrecto.")

# Función para enviar el correo
def enviar_correo(destinatario, codigo):
    load_dotenv()
    remitente = os.getenv("CORREO")
    contraseña = os.getenv("CONTRASENIA")

     # ✨ HTML del correo
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f7; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 30px; text-align: center;">
            <h2 style="color: #c69838;">¡Hola!</h2>
            <p style="font-size: 16px; color: #555;">
                Tu <strong>código de verificación</strong> es:
            </p>
            <div style="font-size: 36px; font-weight: bold; color: #c69838; margin: 20px 0;">
                {codigo}
            </div>
            <p style="font-size: 14px; color: #999;">
                Este código expirará en 10 minutos. No lo compartas con nadie.
            </p>
            <hr style="margin: 30px 0;">
            <p style="font-size: 12px; color: #aaa;">
                © 2025 BeautyAngels — Todos los derechos reservados
            </p>
        </div>
    </body>
    </html>
    """

    # Crear el mensaje
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "Tu código de verificación"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    # Adjuntar el contenido HTML
    mensaje.attach(MIMEText(html, "html"))

    # Enviar
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(remitente, contraseña)
            servidor.sendmail(remitente, destinatario, mensaje.as_string())
        print("✅ Correo enviado con éxito")
    except Exception as e:
        print("❌ Error al enviar el correo:", e)
            

#Obtener datos del usuario
def obtener_datos_usuario(id_auth: str):
    id_usuario = obtener_id_usuario(id_auth)
    
    if not id_usuario or id_usuario == "":
        raise UsuarioError("El id_auth no puede estar vacío o no corresponde a ningún usuario.")
    
    # Llamamos a la función que obtiene los datos por id de usuario
    datos_usuario = obtener_datos_usuario_por_id(id_usuario)

    if not datos_usuario:
        raise UsuarioError("No se encontraron datos para el usuario especificado.")
    
    return datos_usuario


#Obtener agendamientos del usuario 
def obtener_agendamientos(id_auth: str):
    id_usuario = obtener_id_usuario(id_auth)
    if(id_usuario == ""):
        raise UsuarioError("El id no puede estar vacío.")
    else:
        return obtener_agendamientos_por_usuario_id(id_usuario)
    

