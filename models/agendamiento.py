from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import List
from db.queries import obtener_horarios_ocupados, crear_agendamiento_con_tintes, obtener_fechas_horas_por_auth_id
from datetime import datetime
from typing import List, Optional, Dict

#Obtiene las horas disponibles para una fecha dada
def obtener_horas_disponibles(fecha: str):
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        if fecha_obj < datetime.now().date():
            raise HTTPException(status_code=400, detail="Fecha no válida (ya pasó)")

        horas_base = [f"{h:02d}:00" for h in range(8, 21)]
        horas_ocupadas = obtener_horarios_ocupados(fecha)  # lista de strings ["10:00", "15:00"]

        horas_bloqueadas = set()
        for hora in horas_ocupadas:
            ag_inicio = datetime.strptime(hora, "%H:%M")
            for delta in range(-2, 3):
                bloqueada = (ag_inicio + timedelta(hours=delta)).strftime("%H:%M")
                horas_bloqueadas.add(bloqueada)

        horas_validas = [h for h in horas_base if h not in horas_bloqueadas]

        return {"fecha": fecha, "horas": horas_validas}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    

#Valida los datos de un agendamiento sin tocar la base de datos
def validar_datos_agendamiento(fecha, hora, tintes_ids: list, max_tintes: int):
    """
    Valida los datos de un agendamiento SIN tocar la base de datos.
    """
    # 1. Validar tintes
    if tintes_ids:
        if len(tintes_ids) == 0:
            raise HTTPException(status_code=400, detail="Debe elegir al menos un tinte")

        if len(tintes_ids) > max_tintes:
            raise HTTPException(
                status_code=400,
                detail=f"El diseño solo permite {max_tintes} tintes como máximo"
            )

        if len(tintes_ids) != len(set(tintes_ids)):
            raise HTTPException(
                status_code=400,
                detail="Hay tintes repetidos en la lista"
            )

    # 2. Validar fecha y hora
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        hora_obj = datetime.strptime(hora, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha u hora inválido")

    hoy = datetime.now().date()
    if fecha_obj < hoy:
        raise HTTPException(status_code=400, detail="La fecha ya pasó")

    # ✅ Si pasa todo, retorno True
    return True

# Función principal para agendar
def agendar(usuario_id, diseno_id, fecha, hora, tintes_ids, max_tintes):
    # 1. Validar sin DB
    validar_datos_agendamiento(fecha, hora, tintes_ids, max_tintes)

    # 2. Insertar en DB
    return crear_agendamiento_con_tintes(usuario_id, diseno_id, fecha, hora, tintes_ids)

#Funcion para obtener agendamientos de un usuario
def obtener_agendamientos_usuario(usuario_id: int):
  
    return obtener_fechas_horas_por_auth_id(usuario_id)


#Función para obtener el agendamiento más próximo de una lista
def obtener_agendamiento_mas_proximo(agendamientos: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    """
    Retorna el agendamiento con la fecha y hora más próxima (>= ahora).

    Parámetros:
        agendamientos: Lista de dicts con claves 'fecha' (YYYY-MM-DD) y 'hora' (HH:MM).

    Retorna:
        dict | None: El agendamiento más próximo o None si no hay futuros.
    """
    ahora = datetime.now()

    agendamientos_futuros = []
    for ag in agendamientos:
        try:
            fecha_hora = datetime.strptime(f"{ag['fecha']} {ag['hora']}", "%Y-%m-%d %H:%M")
            if fecha_hora >= ahora:
                agendamientos_futuros.append((ag, fecha_hora))
        except ValueError:
            continue  # Ignora agendamientos con formato inválido

    if not agendamientos_futuros:
        return None

    # Retornar el más próximo
    return min(agendamientos_futuros, key=lambda x: x[1])[0]

#Obtener el agendamiento más próximo de un usuario
def obtener_agendamiento_proximo_por_usuario(usuario_id: int) -> Optional[dict]:
    agendamientos = obtener_agendamientos_usuario(usuario_id)
    return obtener_agendamiento_mas_proximo(agendamientos)
