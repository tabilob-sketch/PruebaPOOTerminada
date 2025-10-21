# aplicacion/gestiontipodepartamento.py
from dominio.tipodepartamento import TipoDepartamento
from persistencia.tipodepartamentoDAO import TipoDepartamentoDAO

class GestionTipoDepartamento:
    def __init__(self):
        self.dao = TipoDepartamentoDAO()

    def crear(self, nombre: str) -> int:
        nombre = (nombre or "").strip()
        if len(nombre) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        return self.dao.crear(TipoDepartamento(None, nombre))

    def listar(self):
        return self.dao.listar()

    def obtener(self, id_tipo: int):
        return self.dao.obtener(int(id_tipo))

    def editar(self, id_tipo: int, nombre: str) -> bool:
        return self.dao.actualizar(TipoDepartamento(int(id_tipo), (nombre or "").strip()))

    def eliminar(self, id_tipo: int) -> bool:
        return self.dao.eliminar(int(id_tipo))

