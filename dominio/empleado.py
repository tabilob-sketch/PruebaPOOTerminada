"""Dentro de este archivo se encontrara la clase empleado"""
import datetime
from enum import Enum   
class Empleado:
    
    class TipoEmpleado(Enum): #Definimos a los empleados desde un Enum 
        empleado = "Empleado"    
        administrativo = "Administrativo"
        gerente = "Gerente"

    def __init__(self, id_empleado: int, nombre: str, direccion: str, numero_telefono: int, correo_electronico: str, fecha_inicio_contrato: datetime, salario: int,
                 usuario: str, tipo_empleado: 'Empleado.TipoEmpleado') -> None:
        """Esta clase permite crear objetos de la clase "Empleado" 
        Paramentros:
            id_empleado: int -> corresponde al id de cada empleado el cual es unico y irrepetible
            nombre: str -> corresponde al nombre del empleado
            direccion: str -> corresponde a la direccion de cada empleado
            numero_de_telefono: int -> corresponde al numero de cada empleado
            correo_electronico: str -> corresponde al correo de cada empleado
            fecha_inicio_contrato: datetime -> corresponde a la fecha de contratacion de cada empleado
            salario: int -> corresponde al salario/sueldo de cada empleado
            usuario: str -> corresponde al usuario de cada empleado
            tipo_empleado: Empledao.TipoEmpleado -> corresponde al tipo de empleado que es asignado cada empleado administrador/gerente
        Retorno:
            No contiene retorno
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

    def __str__(self)-> str:
        return f" Empleado: {self.nombre} Tipo empleado: {self.tipo_empleado}"
    # MÉTODOS GETTERS
    def obtener_id(self) -> int:
        return self.id_empleado

    def obtener_nombre(self) -> str:
        return self.nombre

    def obtener_direccion(self) -> str:
        return self.direccion

    def obtener_numero_telefono(self) -> int:
        return self.numero_telefono

    def obtener_correo_electronico(self) -> str:
        return self.correo_electronico

    def obtener_fecha_inicio_contrato(self) -> datetime.datetime:
        return self.fecha_inicio_contrato

    def obtener_salario(self) -> int:
        return self.salario

    def obtener_usuario(self) -> str:
        return self.usuario

    def obtener_tipo_empleado(self) -> str:
        # Usamos .value para obtener la representación en texto del Enum
        return self.tipo_empleado

    # MÉTODOS SETTERS
    def establecer_id(self, id_empleado):
        self.id_empleado = id_empleado