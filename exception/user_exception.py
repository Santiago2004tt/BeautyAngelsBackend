class UsuarioError(Exception):
    pass

class CorreoInvalido(UsuarioError):
    pass

class ContraseniaInvalida(UsuarioError):
    pass

class CampoVacio(UsuarioError):
    pass