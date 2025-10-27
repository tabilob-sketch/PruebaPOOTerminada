# dominio/registrodeturno.py
# ==============================================================
# MODELO DE DOMINIO: RegistroDeTurno
# --------------------------------------------------------------
# Representa un registro de turno de un empleado:
#   - id_registro: identificador del registro (PK en BD)
#   - id_empleado: referencia al empleado (FK o vínculo lógico)
#   - fecha: momento/fecha del turno (datetime)
#   - cantidad_horas: horas trabajadas en el turno (int)
#   - tareas_realizadas: descripción de tareas (str)
# ==============================================================

import datetime

class RegistroDeTurno:
    """
    Clase de dominio (sin lógica de BD) para modelar un registro de turno.
    """

    def __init__(
        self,
        id_registro: int,
        id_empleado: int,
        fecha: datetime.datetime,
        cantidad_horas: int,
        tareas_realizadas: str
    ) -> None:
        """
        Crea una instancia de RegistroDeTurno.

        Parámetros:
            id_registro      : int                -> ID del registro (PK en BD)
            id_empleado      : int                -> ID del empleado asociado (FK)
            fecha            : datetime.datetime  -> Fecha/hora en que se registró el turno
            cantidad_horas   : int                -> Cantidad de horas del turno
            tareas_realizadas: str                -> Descripción de las tareas realizadas
        """
        self.id_registro = id_registro
        self.id_empleado = id_empleado
        self.fecha = fecha
        self.cantidad_horas = cantidad_horas
        self.tareas_realizadas = tareas_realizadas

    def __str__(self) -> str:
        """
        Representación legible del objeto (útil para logs/prints).
        """
        fecha_txt = (
            self.fecha.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(self.fecha, datetime.datetime)
            else str(self.fecha)
        )
        return (
            f"Registro #{self.id_registro} | Empleado {self.id_empleado} | "
            f"Fecha: {fecha_txt} | Horas: {self.cantidad_horas} | "
            f"Tareas: {self.tareas_realizadas}"
        )

    # ----------------------------------------------------------
    # GETTERS
    # ----------------------------------------------------------
    def obtener_id_registro(self) -> int:
        """Retorna el ID del registro (PK)."""
        return self.id_registro

    def obtener_id_empleado(self) -> int:
        """Retorna el ID del empleado asociado (FK)."""
        return self.id_empleado

    def obtener_fecha(self) -> datetime.datetime:
        """Retorna la fecha/hora del turno."""
        return self.fecha

    def obtener_cantidad_horas(self) -> int:
        """Retorna la cantidad de horas del turno."""
        return self.cantidad_horas

    def obtener_tareas_realizadas(self) -> str:
        """Retorna la descripción de las tareas realizadas."""
        return self.tareas_realizadas

    # ----------------------------------------------------------
    # SETTERS opcionales (útiles si actualizas atributos puntuales)
    # ----------------------------------------------------------
    def establecer_id_registro(self, id_registro: int) -> None:
        """Setea el ID del registro (útil al insertar en BD y obtener la PK)."""
        self.id_registro = id_registro

    def establecer_id_empleado(self, id_empleado: int) -> None:
        """Actualiza el ID del empleado asociado al turno."""
        self.id_empleado = id_empleado

    def establecer_fecha(self, fecha: datetime.datetime) -> None:
        """Actualiza la fecha/hora del turno."""
        self.fecha = fecha

    def establecer_cantidad_horas(self, cantidad_horas: int) -> None:
        """Actualiza la cantidad de horas del turno."""
        self.cantidad_horas = cantidad_horas

    def establecer_tareas_realizadas(self, tareas_realizadas: str) -> None:
        """Actualiza la descripción de tareas realizadas."""
        self.tareas_realizadas = tareas_realizadas
