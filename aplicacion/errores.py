# aplicacion/errores.py
class DuplicadoError(Exception):
    """Se intentó insertar/actualizar un valor único ya existente."""
    def __init__(self, campo: str, valor: str):
        super().__init__(f"Valor duplicado en '{campo}': {valor}")
        self.campo = campo
        self.valor = valor

class NoEncontradoError(Exception):
    """Entidad no encontrada."""
    def __init__(self, entidad: str):
        super().__init__(f"{entidad} no encontrado.")

class ValidacionError(Exception):
    """Error de validación de datos de entrada."""
    pass
