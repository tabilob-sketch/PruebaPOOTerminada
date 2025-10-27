# aplicacion/gestiondepartamento.py

# Importamos la clase con el Enum
from dominio.departamento import Departamento
# Importamos el DAO corregido
from persistencia.departamentoDAO import DepartamentoDAO

class gestiondepartamento:
    """
    Clase estática para gestionar los Departamentos.
    Conecta la lógica de dominio (Clase) con la persistencia (DAO).
    """

    # ================== C ==================
    @staticmethod
    def crear_departamento(nombre: str, tipo: Departamento.TipoDepartamento):
        """
        Crea un nuevo departamento.
        Retorna el objeto Departamento creado o None si falla validación.
        """
        nombre_limpio = (nombre or "").strip()
        if len(nombre_limpio) < 3:
            print("Error: El nombre debe tener al menos 3 caracteres.")
            return None

        departamento = Departamento(
            id_departamento=0,
            nombre=nombre_limpio,
            tipo_departamento=tipo
        )
        DepartamentoDAO.guardar_departamento(departamento)
        return departamento

    # ================== U ==================
    @staticmethod
    def editar_departamento(id_departamento: int, nuevo_nombre: str, nuevo_tipo: Departamento.TipoDepartamento):
        """
        Actualiza un departamento existente.
        """
        nombre_limpio = (nuevo_nombre or "").strip()
        if len(nombre_limpio) < 3:
            print("Error: El nombre debe tener al menos 3 caracteres.")
            return

        departamento_actualizado = Departamento(
            id_departamento=int(id_departamento),
            nombre=nombre_limpio,
            tipo_departamento=nuevo_tipo
        )
        DepartamentoDAO.actualizar_departamento(departamento_actualizado)

    # ================== D ==================
    @staticmethod
    def eliminar_departamento(id_departamento: int):
        """
        Elimina un departamento por su ID.
        """
        try:
            id_int = int(id_departamento)
        except ValueError:
            print("Error: ID de departamento inválido.")
            return
        if id_int <= 0:
            print("Error: ID de departamento inválido.")
            return

        DepartamentoDAO.eliminar_departamento(id_int)

    # ================== R (por ID) ==================
    @staticmethod
    def obtener_departamento_por_id(id_departamento: int):
        """
        Busca un departamento por su ID.
        Retorna un dict con: id_departamento, nombre, tipo_departamento; o None si no existe.
        """
        try:
            id_int = int(id_departamento)
        except ValueError:
            print("Error: ID de departamento inválido.")
            return None
        if id_int <= 0:
            print("Error: ID de departamento inválido.")
            return None

        return DepartamentoDAO.obtener_departamento_por_id(id_int)

    # ================== R (listar todos) ==================
    @staticmethod
    def listar_departamentos():
        """
        Retorna una lista de dicts: [{id_departamento, nombre, tipo_departamento}, ...]
        """
        return DepartamentoDAO.listar_departamentos()

    # ================== R (buscar por nombre) ==================
    @staticmethod
    def buscar_departamentos_por_nombre(nombre: str):
        """
        Retorna lista de dicts usando LIKE %nombre% (case-insensitive).
        """
        patron = (nombre or "").strip()
        return DepartamentoDAO.buscar_departamentos_por_nombre(patron)
