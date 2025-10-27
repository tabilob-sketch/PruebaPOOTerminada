# aplicacion/gestiondepartamento.py
# ==============================================================
# CAPA DE APLICACIÓN PARA DEPARTAMENTOS
# --------------------------------------------------------------
# Esta capa conecta la presentación (inputs del usuario) con:
#   - La lógica de dominio (clase Departamento con su Enum).
#   - La persistencia (DepartamentoDAO que habla con la BD).
#
# Responsabilidades:
#   * Validar/normalizar entradas (por ejemplo, nombre con largo mínimo).
#   * Construir objetos de dominio coherentes.
#   * Delegar las operaciones CRUD al DAO.
# ==============================================================

# Importamos la clase con el Enum (modelo de dominio)
from dominio.departamento import Departamento
# Importamos el DAO que hace las consultas a BD
from persistencia.departamentoDAO import DepartamentoDAO

class gestiondepartamento:
    """
    Clase estática de “servicio” para gestionar Departamentos.
    No mantiene estado (solo métodos @staticmethod) y actúa de puente
    entre la capa de presentación y el DAO.
    """

    # ================== C  (CREATE) ==================
    @staticmethod
    def crear_departamento(nombre: str, tipo: Departamento.TipoDepartamento):
        """
        Crea un nuevo departamento.
        - Valida que el nombre tenga un largo mínimo razonable.
        - Construye el objeto de dominio Departamento.
        - Llama al DAO para persistirlo.
        Retorna:
            * El objeto Departamento creado si pasa la validación.
            * None si la validación falla (y se imprime el motivo).
        """
        # Normalizamos el nombre: eliminamos espacios y revisamos largo
        nombre_limpio = (nombre or "").strip()
        if len(nombre_limpio) < 3:
            print("Error: El nombre debe tener al menos 3 caracteres.")
            return None

        # Construimos el objeto de dominio; id_departamento=0 porque la BD lo genera (AUTO_INCREMENT)
        departamento = Departamento(
            id_departamento=0,
            nombre=nombre_limpio,
            tipo_departamento=tipo
        )

        # Delegamos el INSERT al DAO (maneja conexión y SQL)
        DepartamentoDAO.guardar_departamento(departamento)

        # Devolvemos el objeto por si la capa superior quiere mostrarlo/usar su info
        return departamento

    # ================== U  (UPDATE) ==================
    @staticmethod
    def editar_departamento(id_departamento: int, nuevo_nombre: str, nuevo_tipo: Departamento.TipoDepartamento):
        """
        Actualiza un departamento existente.
        - Valida el nuevo nombre (mismo criterio de creación).
        - Prepara un objeto Departamento con los datos actualizados.
        - Llama al DAO para ejecutar el UPDATE en BD.
        No retorna nada; en caso de error de validación informa por consola.
        """
        nombre_limpio = (nuevo_nombre or "").strip()
        if len(nombre_limpio) < 3:
            print("Error: El nombre debe tener al menos 3 caracteres.")
            return

        # Creamos un objeto con el ID existente y los nuevos valores
        departamento_actualizado = Departamento(
            id_departamento=int(id_departamento),  # nos aseguramos que sea int
            nombre=nombre_limpio,
            tipo_departamento=nuevo_tipo
        )

        # Delegamos el UPDATE al DAO
        DepartamentoDAO.actualizar_departamento(departamento_actualizado)

    # ================== D  (DELETE) ==================
    @staticmethod
    def eliminar_departamento(id_departamento: int):
        """
        Elimina un departamento por su ID (ELIMINACIÓN en bd).
        - Valida que el ID sea un entero positivo.
        - Llama al DAO para hacer el DELETE.
        """
        # Convertimos a int y validamos rango
        try:
            id_int = int(id_departamento)
        except ValueError:
            print("Error: ID de departamento inválido.")
            return
        if id_int <= 0:
            print("Error: ID de departamento inválido.")
            return

        # Delegamos el DELETE al DAO
        DepartamentoDAO.eliminar_departamento(id_int)

    # ================== R  (READ por ID) ==================
    @staticmethod
    def obtener_departamento_por_id(id_departamento: int):
        """
        Busca un departamento por su ID.
        - Valida el ID.
        - Retorna un dict con {id_departamento, nombre, tipo_departamento} si existe;
          o None si no se encuentra / el ID no es válido.
        """
        # Validación básica del ID
        try:
            id_int = int(id_departamento)
        except ValueError:
            print("Error: ID de departamento inválido.")
            return None
        if id_int <= 0:
            print("Error: ID de departamento inválido.")
            return None

        # Delegamos la búsqueda al DAO (SELECT ... WHERE id=...)
        return DepartamentoDAO.obtener_departamento_por_id(id_int)

    # ================== R  (READ listar todos) ==================
    @staticmethod
    def listar_departamentos():
        """
        Lista todos los departamentos.
        Retorna:
            Lista de dicts con la forma:
            [{ 'id_departamento': ..., 'nombre': ..., 'tipo_departamento': ... }, ...]
        (El formato exacto depende de cómo lo arme el DAO).
        """
        return DepartamentoDAO.listar_departamentos()

    # ================== R  (READ buscar por nombre) ==================
    @staticmethod
    def buscar_departamentos_por_nombre(nombre: str):
        """
        Busca departamentos cuyo nombre coincida parcialmente (LIKE %nombre%).
        - Limpia el texto de búsqueda.
        - Delegá en el DAO el SELECT con LIKE y case-insensitive (si el DAO lo implementa así).
        Retorna:
            Lista de dicts similar a listar_departamentos(), pero filtrada.
        """
        patron = (nombre or "").strip()
        return DepartamentoDAO.buscar_departamentos_por_nombre(patron)
