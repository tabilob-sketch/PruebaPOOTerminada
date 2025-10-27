# dominio/departamento.py
# ==============================================================
# MODELO DE DOMINIO: Departamento
# --------------------------------------------------------------
# Representa un departamento de la organización.
# Incluye:
#   - Un Enum con los tipos válidos de departamento.
#   - Atributos básicos (id, nombre, tipo).
#   - Métodos de acceso (getters/setters) y __str__ para imprimir.
# ==============================================================

from enum import Enum

class Departamento:
    """
    Clase de dominio (POO) que modela un Departamento.
    No contiene lógica de BD; solo datos y comportamiento básico.
    """

    class TipoDepartamento(Enum):
        """
        Enumeración de tipos válidos de departamento.
        Usar siempre estas opciones (evita strings sueltos/errores de tipeo).
        El .value es el texto 'humano' que puedes guardar/mostrar.
        """
        desarrollo_sostenible = "Desarrollo Sostenible"
        investigacion = "Investigacion"
        desarrollo = "Desarrollo"
        ventas = "Ventas"
        recursos_humanos = "Recursos Humanos"

    def __init__(self, id_departamento: int, nombre: str, tipo_departamento: 'Departamento.TipoDepartamento') -> None:
        """
        Crea una instancia de Departamento.

        Parámetros:
            id_departamento : int
                ID en la BD. Cuando aún no existe en BD, se recomienda usar 0 (o None)
                y luego setearlo con establecer_id_departamento cuando el DAO devuelva el ID.
            nombre : str
                Nombre del departamento (ej: "Innovación", "Soporte").
            tipo_departamento : Departamento.TipoDepartamento
                Uno de los valores del Enum TipoDepartamento.
        """
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.tipo_departamento = tipo_departamento

    def __str__(self) -> str:
        """
        Representación legible del objeto (útil para prints/logs).
        Muestra el nombre y el tipo (como Enum; si deseas el texto, usa .value).
        """
        return f"Nombre: {self.nombre}, Tipo de departamento: {self.tipo_departamento.value}"

    # ----------------------------------------------------------
    # GETTERS (métodos de lectura)
    # ----------------------------------------------------------

    def obtener_id_departamento(self) -> int:
        """
        Retorna el ID del departamento.
        Será 0 (o None, si así lo usas) si todavía no se insertó en la BD.
        """
        return self.id_departamento

    def obtener_nombre(self) -> str:
        """Retorna el nombre del departamento."""
        return self.nombre

    def obtener_tipo_departamento(self) -> 'Departamento.TipoDepartamento':
        """
        Retorna el OBJETO Enum del tipo de departamento.
        Si necesitas el texto para guardar/mostrar, usa .value
        (ej.: self.obtener_tipo_departamento().value)
        """
        return self.tipo_departamento

    # ----------------------------------------------------------
    # SETTERS (métodos de escritura/actualización)
    # ----------------------------------------------------------

    def establecer_id_departamento(self, id_departamento: int) -> None:
        """
        Establece el ID del departamento (útil después de un INSERT en BD).
        Normalmente lo invoca el DAO cuando la BD devuelve el nuevo ID.
        """
        self.id_departamento = id_departamento

    def establecer_nombre(self, nombre: str) -> None:
        """
        Actualiza el nombre del departamento.
        Puedes agregar validaciones aquí (mínimo largo, caracteres, etc.)
        si lo prefieres en la capa de dominio.
        """
        self.nombre = nombre

    def establecer_tipo_departamento(self, tipo_departamento: 'Departamento.TipoDepartamento') -> None:
        """
        Actualiza el tipo de departamento usando el Enum.
        Recomendado: siempre recibir un Enum y no un string.
        """
        self.tipo_departamento = tipo_departamento
