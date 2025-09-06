
import re


# Funciones de servicio relacionadas con usuarios


# Servicio para validar la fortaleza de una contraseña.
def verificar_contrasenia_escrito(password: str) -> bool:
    """
    Verifica si una contraseña cumple con los criterios de seguridad:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    - Al menos un carácter especial
    """
    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):  # Mayúscula
        return False

    if not re.search(r"[a-z]", password):  # Minúscula
        return False

    if not re.search(r"[0-9]", password):  # Número
        return False

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", password):  # Especial
        return False

    return True


#servicio para validar el formato de un correo electrónico.
def verificar_email(email: str) -> bool:
    """
    Verifica si un correo electrónico tiene un formato válido.
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None




