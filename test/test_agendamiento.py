from db.queries import crear_agendamiento, crear_agendamiento_con_tintes
from models.agendamiento import agendar
import os

def test_crear_agendamiento():
    try:
        agendamiento = crear_agendamiento(
            usuario_id="5373cf70-79b4-4c66-ac92-b611438716e2",
            diseno_id="be6c866b-8c55-4687-b93d-c2da8da63386",
            fecha="2025-09-01",
            hora="10:00"
        )
        print("Agendamiento creado:", agendamiento)
    except Exception as e:
        assert False, f"Error al crear agendamiento: {str(e)}"


def test_crear_agendamiento_con_tintes():
    try:
        agendamiento = crear_agendamiento_con_tintes(
            usuario_id="5373cf70-79b4-4c66-ac92-b611438716e2",
            diseno_id="be6c866b-8c55-4687-b93d-c2da8da63386",
            fecha="2025-09-01",
            hora="11:00",
            tintes_ids=["02bf77e4-8c62-4cea-9fff-087ddea4f271"]
        )
        print("Agendamiento con tintes creado:", agendamiento)
    except Exception as e:
        assert False, f"Error al crear agendamiento con tintes: {str(e)}"

def agendar_test():
    try:
        agendamiento = agendar(
            "0bfd1f2a-b94f-4ed5-99e0-2420087021fe",
            "54e2edfd-3105-4788-b2aa-639e3e161813",
            "2025-09-10",
            "11:00",
            ["02bf77e4-8c62-4cea-9fff-087ddea4f271"],
            1
        )
        print("Agendamiento con tintes creado:", agendamiento)
    except Exception as e:
        assert False, f"Error al crear agendamiento con tintes: {str(e)}"

agendar_test()