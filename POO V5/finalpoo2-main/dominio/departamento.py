"""Dentro de este archivo se encontrara la clase departamento"""
from enum import Enum

class Departamento:
    
    class TipoDepartamento(Enum):
        desarrollo_sostenible = "Desarrollo Sostenible"
        investigacion = "Investigacion"
        desarrollo = "Desarrollo"
        ventas = "Ventas"
        recursos_humanos = "Recursos Humanos"

    def __init__(self, id_departamento: int, nombre: str, tipo_departamento: 'Departamento.TipoDepartamento') -> None:
        """
        Esta clase permite crear objetos de la clase Departamento
        Parametros: 
            id_departamento: int -> ID de la BD. Usar 0 si es un objeto nuevo.
            nombre: str -> corresponde al nombre de cada departamento
            tipo_departamento: Departamento.TipoDepartamento -> corresponde al Enum del tipo
        """
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.tipo_departamento = tipo_departamento

    def __str__(self) -> str:
            return f"Nombre {self.nombre}, Tipo de departamento: {self.tipo_departamento}"

    # --- MÉTODOS GETTERS ---

    def obtener_id_departamento(self) -> int: 
        """
        Retorna el ID del departamento.
        Será 0 si el objeto aún no se ha guardado en la BD.
        """
        return self.id_departamento

    def obtener_nombre(self) -> str:
        """
        Retorna el nombre del departamento.
        """
        return self.nombre

    def obtener_tipo_departamento(self) -> 'Departamento.TipoDepartamento':
        """
        Retorna el OBJETO Enum del tipo de departamento.
        """
        return self.tipo_departamento

    # --- MÉTODOS SETTERS ---

    def establecer_id_departamento(self, id_departamento: int) -> None: 
        """
        Establece el ID del departamento (usado después de insertar en BD).
        """
        self.id_departamento = id_departamento

    def establecer_nombre(self, nombre: str) -> None:
        """
        Actualiza el nombre del departamento.
        """
        self.nombre = nombre

    def establecer_tipo_departamento(self, tipo_departamento: 'Departamento.TipoDepartamento') -> None:
        """
        Actualiza el tipo de departamento usando el Enum.
        """
        self.tipo_departamento = tipo_departamento