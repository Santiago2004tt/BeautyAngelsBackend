from exception.user_exception import (
    UsuarioError,
    CorreoInvalido,
    ContraseniaInvalida,
    CampoVacio,
)
from models.user_service import verificar_contrasenia_escrito, verificar_email
from db.queries import registrar_usuario, iniciar_sesion, obtener_nombre_usuario


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

def login_usuario(correo: str, password: str):
    if not correo or not correo.strip():
        raise CampoVacio("El campo 'correo' no puede estar vacío.")
    if not password or not password.strip():
        raise CampoVacio("El campo 'contraseña' no puede estar vacío.") 
    if (not verificar_email(correo)) :
        raise CorreoInvalido("El correo no cumple con el formato adecuado.")
    iniciar_sesion(correo, password)

def obtener_nombre(id: str):
    if not id:
        raise CampoVacio("El campo 'id' no puede estar vacío.")
    else:
        return obtener_nombre_usuario(id)