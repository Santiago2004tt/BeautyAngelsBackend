from db.queries import obtener_disenos, obtener_disenos_por_id, obtener_horarios_ocupados
from models.agendamiento import horas_disponibles


def obtener_diseno_test():
    disenos = obtener_disenos()
    return 

def obtener_diseno_por_id_test(disenio_id):
    diseno = obtener_disenos_por_id(disenio_id)
   
    return diseno

def obtener_horarios_ocupados_test(fecha):
    
    horarios = obtener_horarios_ocupados(fecha)
    return horarios

def obtener_horarios_libre_test(fecha):
    
    horarios = horas_disponibles(fecha)
    return horarios

print(obtener_horarios_libre_test("2025-09-05"))

