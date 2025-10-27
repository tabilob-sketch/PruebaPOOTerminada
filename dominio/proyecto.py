# dominio/proyecto.py
# ==============================================================
# MODELO DE DOMINIO: Proyecto
# --------------------------------------------------------------
# Representa un proyecto de la organización.
# Incluye:
#   - Atributos básicos (id, nombre, descripción, fecha_inicio).
#   - Relación con Empleado(s) asignados (lista en memoria).
#   - Métodos utilitarios: crear/editar/eliminar (a nivel de dominio),
#     asignar y desasignar empleados.
# Nota: aquí NO hay acceso a BD; eso vive en la capa de persistencia (DAO).
# ==============================================================

import datetime
from dominio.empleado import Empleado

class Proyecto:
    """
    Clase de dominio que modela un Proyecto.
    No maneja SQL ni conexiones; solo datos y comportamiento básico.
    """

    def __init__(
        self,
        id_proyecto: int,
        nombre: str,
        descripcion: str,
        fecha_inicio: datetime.datetime
    ) -> None:
        """
        Crea una instancia de Proyecto.

        Parámetros:
            id_proyecto  : int
                ID del proyecto en la BD. Puede ser 0/None si aún no existe en BD
                y se establecerá luego con establecer_id().
            nombre       : str
                Nombre del proyecto.
            descripcion  : str
                Descripción del proyecto.
            fecha_inicio : datetime.datetime
                Fecha (y opcionalmente hora) de inicio del proyecto.
        """
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

        # Relación a nivel de dominio (en memoria): lista de Empleado asignados
        self.empleados_asignados: list[Empleado] = []

    # ----------------------------------------------------------
    # Representación legible
    # ----------------------------------------------------------
    def __str__(self) -> str:
        """
        Representación útil para prints/logs.
        """
        fecha_txt = (
            self.fecha_inicio.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(self.fecha_inicio, datetime.datetime)
            else str(self.fecha_inicio)
        )
        return (
            f"ID: {self.id_proyecto}, "
            f"Proyecto: {self.nombre}, "
            f"Descripción: {self.descripcion}, "
            f"Inicio: {fecha_txt}"
        )

    # ----------------------------------------------------------
    # GETTERS
    # ----------------------------------------------------------
    def obtener_id(self) -> int:
        """Retorna el ID del proyecto (PK en BD)."""
        return self.id_proyecto

    def obtener_nombre(self) -> str:
        """Retorna el nombre del proyecto."""
        return self.nombre

    def obtener_descripcion(self) -> str:
        """Retorna la descripción del proyecto."""
        return self.descripcion

    def obtener_fecha_inicio(self) -> datetime.datetime:
        """Retorna la fecha de inicio como datetime."""
        return self.fecha_inicio

    # ----------------------------------------------------------
    # SETTERS (útiles para actualizar atributos puntuales)
    # ----------------------------------------------------------
    def establecer_id(self, id_proyecto: int) -> None:
        """
        Establece el ID del proyecto (útil luego de insertar en BD y obtener la PK).
        """
        self.id_proyecto = id_proyecto

    def establecer_nombre(self, nuevo_nombre: str) -> None:
        """Actualiza el nombre del proyecto."""
        self.nombre = nuevo_nombre

    def establecer_descripcion(self, nueva_descripcion: str) -> None:
        """Actualiza la descripción del proyecto."""
        self.descripcion = nueva_descripcion

    def establecer_fecha_inicio(self, nueva_fecha: datetime.datetime) -> None:
        """Actualiza la fecha de inicio del proyecto."""
        self.fecha_inicio = nueva_fecha

    # ----------------------------------------------------------
    # Métodos de “ciclo de vida” (nivel de dominio)
    # ----------------------------------------------------------
    def nuevoProyecto(self) -> None:
        """
        Hook o método informativo: puede usarse para lógica adicional
        cuando “nace” un proyecto (logs, validaciones extra, etc.).
        """
        print(f"Proyecto '{self.nombre}' creado exitosamente.")

    def editarProyecto(self, nuevo_nombre: str | None = None, nueva_descripcion: str | None = None) -> None:
        """
        Actualiza campos básicos del proyecto en memoria.
        (La persistencia real la hace el DAO de proyectos.)
        """
        if nuevo_nombre:
            self.nombre = nuevo_nombre
        if nueva_descripcion:
            self.descripcion = nueva_descripcion
        print(f"Proyecto '{self.nombre}' actualizado.")

    def eliminarProyecto(self) -> None:
        """
        Hook informativo: a nivel de dominio indica eliminación.
        (La eliminación real en BD la hace el DAO).
        """
        print(f"Proyecto '{self.nombre}' eliminado.")

    # ----------------------------------------------------------
    # Relación con Empleados: asignar / desasignar
    # ----------------------------------------------------------
    def asignar_empleado(self, empleado: Empleado) -> None:
        """
        Asigna un empleado al proyecto, si no estaba ya asignado.
        """
        if empleado not in self.empleados_asignados:
            self.empleados_asignados.append(empleado)
            print(f"Empleado '{empleado.nombre}' asignado a proyecto '{self.nombre}'.")
        else:
            print(f"Empleado '{empleado.nombre}' ya estaba asignado a este proyecto.")

    def desasignar_empleado(self, empleado: Empleado) -> None:
        """
        Desasigna un empleado del proyecto, si estaba asignado.
        """
        if empleado in self.empleados_asignados:
            self.empleados_asignados.remove(empleado)
            print(f"Empleado '{empleado.nombre}' desasignado de proyecto '{self.nombre}'.")
        else:
            print(f"Empleado '{empleado.nombre}' no está asignado a este proyecto.")
