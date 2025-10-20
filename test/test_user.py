import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from models.user_service import verificar_contrasenia_escrito


# --- Tests generales válidos ---
def test_contrasenias_validas():
    assert verificar_contrasenia_escrito("Hola123!") is True
    assert verificar_contrasenia_escrito("Password123!") is True
    assert verificar_contrasenia_escrito("Pass_word1") is True
    assert verificar_contrasenia_escrito("Contra$3ña") is True
    assert verificar_contrasenia_escrito("Aa1!Aa1!") is True


# --- Tests por longitud ---
def test_contrasenias_demasiado_cortas():
    assert verificar_contrasenia_escrito("Ho1!") is False
    assert verificar_contrasenia_escrito("Aa1!") is False
    assert verificar_contrasenia_escrito("") is False
    assert verificar_contrasenia_escrito("        ") is False


# --- Tests por mayúsculas ---
def test_sin_mayusculas():
    assert verificar_contrasenia_escrito("hola123!") is False
    assert verificar_contrasenia_escrito("contra$3ña") is False


# --- Tests por minúsculas ---
def test_sin_minusculas():
    assert verificar_contrasenia_escrito("HOLA123!") is False
    assert verificar_contrasenia_escrito("PASS123@") is False


# --- Tests por números ---
def test_sin_numeros():
    assert verificar_contrasenia_escrito("Hola!@#") is False
    assert verificar_contrasenia_escrito("Password!") is False


# --- Tests por carácter especial ---
def test_sin_caracter_especial():
    assert verificar_contrasenia_escrito("Hola1234") is False
    assert verificar_contrasenia_escrito("Password123") is False


# --- Tests solo números o letras ---
def test_solo_numeros_o_letras():
    assert verificar_contrasenia_escrito("12345678") is False
    assert verificar_contrasenia_escrito("Holamundo") is False


# --- Tests mixtos/extremos ---
def test_contrasenias_extremas():
    # muy larga pero válida
    assert verificar_contrasenia_escrito("SuperLargaPassword123!!!") is True
    # solo símbolos
    assert verificar_contrasenia_escrito("!!!!!!!!") is False
    # mezcla pero sin número
    assert verificar_contrasenia_escrito("MixDeCosas!") is False