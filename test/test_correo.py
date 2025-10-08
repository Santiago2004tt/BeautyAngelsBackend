import pytest
from models.user import enviar_correo, verificar_codigo

def test_enviar_codigo_verificacion():
    enviar_correo("santisbb2004@gmail.com", "1234")
    assert True  # Si no hay excepción, la prueba pasa

def test_verificar_codigo():
    verificar_codigo("f4f49993-47d7-484b-a1e2-16e8d154b689", "1111")
    assert True  # Si no hay excepción, la prueba pasa
    
