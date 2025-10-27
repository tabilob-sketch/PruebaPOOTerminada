"""Dentro de este archivo se encontrara la clase informe"""
from enum import Enum

class Informe:
    class TipoInforme(Enum):
        pdf = "PDF"
        word = "Word"
        excel = "Excel"

    def __init__(self, tipo_informe: 'Informe.TipoInforme') -> None:
        """Esta clase permite crear objetos de la clase Informe
        Parametros:
            tipo_informe: str -> corresponde al tipo de informe que realice
        Retorno:
            No contiene retorno
        """
        self.tipo_informe = tipo_informe

        def __str__(self) -> str:
            return f"Informe del tipo: {self.tipo_informe}"