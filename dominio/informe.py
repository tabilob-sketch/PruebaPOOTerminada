# dominio/informe.py
# ==============================================================
# MODELO DE DOMINIO: Informe
# --------------------------------------------------------------
# Representa un informe con un tipo específico (PDF, Word, Excel).
# Usa un Enum para estandarizar los tipos y evitar errores de tipeo.
# ==============================================================

from enum import Enum

class Informe:
    """
    Clase de dominio que modela un Informe.
    No maneja base de datos; solo datos y comportamiento básico.
    """

    class TipoInforme(Enum):
        """
        Tipos válidos de informe. Usa estos valores siempre
        (en vez de strings sueltos) para mantener consistencia.
        """
        pdf = "PDF"
        word = "Word"
        excel = "Excel"

    def __init__(self, tipo_informe: 'Informe.TipoInforme') -> None:
        """
        Crea una instancia de Informe.

        Parámetros:
            tipo_informe : Informe.TipoInforme
                Valor del Enum que indica el tipo de informe (PDF/Word/Excel).
        """
        self.tipo_informe = tipo_informe

    def __str__(self) -> str:
        """
        Representación legible del objeto (útil en prints/logs).
        Muestra el tipo en texto humano (usando .value del Enum).
        """
        # Si es Enum, usamos .value; si ya es string, lo mostramos tal cual.
        tipo_txt = self.tipo_informe.value if isinstance(self.tipo_informe, Informe.TipoInforme) else str(self.tipo_informe)
        return f"Informe del tipo: {tipo_txt}"

    # ----------------------------
    # GETTER / SETTER opcionales
    # ----------------------------

    def obtener_tipo_informe(self) -> 'Informe.TipoInforme':
        """Retorna el OBJETO Enum del tipo de informe."""
        return self.tipo_informe

    def establecer_tipo_informe(self, tipo_informe: 'Informe.TipoInforme') -> None:
        """Actualiza el tipo de informe (debe ser un valor del Enum TipoInforme)."""
        self.tipo_informe = tipo_informe
