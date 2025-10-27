# dominio/empleado.py
# ==============================================================
# MODELO DE DOMINIO: Empleado
# --------------------------------------------------------------
# Representa a un empleado de la organización.
# Incluye:
#   - Un Enum con los tipos válidos de empleado.
#   - Atributos básicos (id, nombre, dirección, teléfono, correo, etc.).
#   - Métodos de acceso (getters/setters) y __str__ para impresión legible.
# ==============================================================

import datetime
from enum import Enum

class Empleado:
    """
    Clase de dominio que modela un Empleado.
    No contiene lógica de BD; solo datos y comportamiento básico.
    """

    class TipoEmpleado(Enum):
        """
        Enumeración con los tipos válidos de empleado.
        Usar siempre estas opciones (evita strings sueltos/errores de tipeo).
        El .value entrega el texto “humano” que puedes mostrar/guardar.
        """
        empleado = "Empleado"
        administrativo = "Administrativo"
        gerente = "Gerente"

    def __init__(
        self,
        id_empleado: int,
        nombre: str,
        direccion: str,
        numero_telefono: int,
        correo_electronico: str,
        fecha_inicio_contrato: datetime.datetime,
        salario: int,
        usuario: str,
        tipo_empleado: 'Empleado.TipoEmpleado'
    ) -> None:
        """
        Crea una instancia de Empleado.

        Parámetros:
            id_empleado : int
                ID único del empleado en la BD (PK). Si aún no existe en BD,
                puedes usar 0 o None y asignarlo luego con el setter.
            nombre : str
                Nombre del empleado.
            direccion : str
                Dirección del empleado.
            numero_telefono : int
                Número de teléfono. (Si prefieres guardar texto con +56, espacios, etc.,
                puedes usar str en vez de int a nivel de proyecto.)
            correo_electronico : str
                Correo del empleado.
            fecha_inicio_contrato : datetime.datetime
                Fecha/hora de inicio del contrato.
            salario : int
                Salario/sueldo del empleado. (Si manejas decimales, úsalo como float/Decimal.)
            usuario : str
                Usuario/cuenta asociada al empleado.
            tipo_empleado : Empleado.TipoEmpleado
                Tipo del empleado según el Enum (Empleado/Administrativo/Gerente).

        Retorno:
            No aplica (constructor).
        """
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.direccion = direccion
        self.numero_telefono = numero_telefono
        self.correo_electronico = correo_electronico
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario
        self.usuario = usuario
        self.tipo_empleado = tipo_empleado

    def __str__(self) -> str:
        """
        Representación legible del objeto (útil para prints/logs).
        Muestra nombre y el tipo en texto (usando .value del Enum).
        """
        # Si tipo_empleado es Enum, mostramos su .value (texto "humano")
        tipo_txt = self.tipo_empleado.value if isinstance(self.tipo_empleado, Empleado.TipoEmpleado) else str(self.tipo_empleado)
        return f"Empleado: {self.nombre} | Tipo: {tipo_txt}"

    # ----------------------------------------------------------
    # MÉTODOS GETTERS (lectura)
    # ----------------------------------------------------------

    def obtener_id(self) -> int:
        """Retorna el ID del empleado (PK en la BD)."""
        return self.id_empleado

    def obtener_nombre(self) -> str:
        """Retorna el nombre del empleado."""
        return self.nombre

    def obtener_direccion(self) -> str:
        """Retorna la dirección del empleado."""
        return self.direccion

    def obtener_numero_telefono(self) -> int:
        """
        Retorna el número de teléfono (tal como fue almacenado).
        Nota: si decides manejar formatos internacionales con '+56' u otros,
        convendría tipar este atributo como str en todo el proyecto.
        """
        return self.numero_telefono

    def obtener_correo_electronico(self) -> str:
        """Retorna el correo electrónico del empleado."""
        return self.correo_electronico

    def obtener_fecha_inicio_contrato(self) -> datetime.datetime:
        """Retorna la fecha/hora de inicio del contrato (datetime)."""
        return self.fecha_inicio_contrato

    def obtener_salario(self) -> int:
        """
        Retorna el salario del empleado.
        Nota: si manejas decimales (bonos, céntimos), considerar float/Decimal.
        """
        return self.salario

    def obtener_usuario(self) -> str:
        """Retorna el usuario/cuenta asociada del empleado."""
        return self.usuario

    def obtener_tipo_empleado(self) -> 'Empleado.TipoEmpleado':
        """
        Retorna el OBJETO Enum del tipo de empleado.
        Si necesitas el texto para mostrar/guardar, usa .value, por ejemplo:
            self.obtener_tipo_empleado().value  -> "Gerente"
        """
        return self.tipo_empleado

    # ----------------------------------------------------------
    # MÉTODOS SETTERS (escritura/actualización)
    # ----------------------------------------------------------

    def establecer_id(self, id_empleado: int) -> None:
        """
        Establece el ID del empleado (útil después de insertar en BD cuando la PK es autogenerada).
        """
        self.id_empleado = id_empleado
