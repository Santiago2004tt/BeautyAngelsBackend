import pytest
from models.user import enviar_correo, verificar_codigo,generar_codigo_verificacion , verificar_codigo, obtener_datos_usuario
from models.agendamiento import obtener_agendamiento_proximo_por_usuario

def test_enviar_codigo_verificacion():
    enviar_correo("santisbb2004@gmail.com", "1234")
    assert True  # Si no hay excepción, la prueba pasa

def test_verificar_codigo():
    verificar_codigo("f4f49993-47d7-484b-a1e2-16e8d154b689", "1111")
    assert True  # Si no hay excepción, la prueba pasa


b=obtener_agendamiento_proximo_por_usuario("40ffcf88-aae4-4667-b603-d962cd162ab5")

#enviar_correo("luisan.rengifof@uqvirtual.edu.co", "1113")

#generar_codigo_verificacion("40ffcf88-aae4-4667-b603-d962cd162ab5")

#b= verificar_codigo("49028fb0-29d2-43ec-a97c-7f0abcec23d0", "7359")
#print(b)

#b = obtener_datos_usuario("40ffcf88-aae4-4667-b603-d962cd162ab5")
#print(b)