import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from models.user_service import verificar_email

# --- Tests válidos ---
def test_emails_validos():
    assert verificar_email("usuario@gmail.com") is True
    assert verificar_email("nombre.apellido@dominio.com") is True
    assert verificar_email("user123@empresa.co") is True
    assert verificar_email("mi_correo+test@sub.dominio.org") is True
    assert verificar_email("correo@dominio.io") is True


# --- Tests sin arroba ---
def test_sin_arroba():
    assert verificar_email("usuariogmail.com") is False
    assert verificar_email("correo.dominio.com") is False


# --- Tests con dominio inválido ---
def test_dominio_invalido():
    assert verificar_email("usuario@") is False
    assert verificar_email("usuario@dominio") is False
    assert verificar_email("usuario@dominio.") is False


# --- Tests con caracteres inválidos ---
def test_caracteres_invalidos():
    assert verificar_email("usuario!@gmail.com") is False
    assert verificar_email("user#name@domain.com") is False
    assert verificar_email("user space@domain.com") is False


# --- Tests extremos ---
def test_casos_extremos():
    assert verificar_email("") is False                    # vacío
    assert verificar_email("   ") is False                 # espacios
    assert verificar_email("@gmail.com") is False          # sin usuario
    assert verificar_email("usuario@.com") is False        # dominio sin nombre
    assert verificar_email("usuario@dominio.c") is False   # dominio con TLD muy corto
    assert verificar_email("usuario@dominio.toolongtld") is True  # TLD largo pero válido