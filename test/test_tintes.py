import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from models.agendamiento import validar_datos_agendamiento


# --- Tests exitosos ---
def test_agendamiento_valido():
    fecha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    hora = "14:30"
    assert validar_datos_agendamiento(fecha, hora, [1, 2], 3) is True


# --- Tests de fecha y hora ---
def test_fecha_invalida():
    with pytest.raises(HTTPException) as exc:
        validar_datos_agendamiento("2024-99-99", "14:30", [1], 3)
    assert exc.value.status_code == 400
    assert "Formato" in exc.value.detail

def test_hora_invalida():
    with pytest.raises(HTTPException) as exc:
        validar_datos_agendamiento("2025-10-20", "25:61", [1], 3)
    assert exc.value.status_code == 400
    assert "Formato" in exc.value.detail

def test_fecha_pasada():
    fecha_pasada = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    with pytest.raises(HTTPException) as exc:
        validar_datos_agendamiento(fecha_pasada, "10:00", [1], 3)
    assert exc.value.status_code == 400
    assert "pasó" in exc.value.detail



def test_tintes_excedidos():
    fecha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    with pytest.raises(HTTPException) as exc:
        validar_datos_agendamiento(fecha, "10:00", [1, 2, 3, 4], 3)
    assert exc.value.status_code == 400
    assert "máximo" in exc.value.detail

def test_tintes_repetidos():
    fecha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    with pytest.raises(HTTPException) as exc:
        validar_datos_agendamiento(fecha, "10:00", [1, 2, 2], 3)
    assert exc.value.status_code == 400
    assert "repetidos" in exc.value.detail