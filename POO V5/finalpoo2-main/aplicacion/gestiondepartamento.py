# Importamos la clase con el Enum
from dominio.departamento import Departamento 
# Importamos el DAO corregido que usa objetos
from persistencia.departamentoDAO import DepartamentoDAO 
# 'Optional' y 'List' ya no se importan de 'typing'

class gestiondepartamento:
    """
    Clase estática para gestionar los Departamentos.
    Conecta la lógica de dominio (Clase) con la persistencia (DAO).
    """

    @staticmethod
    def crear_departamento(nombre: str, tipo: Departamento.TipoDepartamento) -> Departamento:
        """
        Crea un nuevo departamento.
        
        Parametros:
            nombre (str): Nombre para el nuevo departamento.
            tipo (Departamento.TipoDepartamento): El Enum del tipo.
        
        Retorno:
            El objeto Departamento creado (con el ID actualizado por el DAO) o None si falla.
        """
        # 1. Validación
        nombre_limpio = (nombre or "").strip()
        if len(nombre_limpio) < 3:
            print("Error: El nombre debe tener al menos 3 caracteres.")
            return None
        
        # 2. Creamos el objeto (ID 0 como temporal, como definimos)
        departamento = Departamento(
            id_departamento=0, 
            nombre=nombre_limpio, 
            tipo_departamento=tipo
        )
        
        # 3. Llamamos al DAO estático
        DepartamentoDAO.guardar_departamento(departamento)
        
        # 4. Retornamos el objeto
        return departamento

    """---------------------------------------------------------------------------------------------------------------------"""

    @staticmethod
    def editar_departamento(id_departamento: int, nuevo_nombre: str, nuevo_tipo: Departamento.TipoDepartamento):
        """
        Actualiza un departamento existente.
        """
        # 1. Validación
        nombre_limpio = (nuevo_nombre or "").strip()
        if len(nombre_limpio) < 3:
            print("Error: El nombre debe tener al menos 3 caracteres.")
            return
        
        # 2. Creamos el objeto con los datos completos
        departamento_actualizado = Departamento(
            id_departamento=id_departamento,
            nombre=nombre_limpio,
            tipo_departamento=nuevo_tipo
        )
        
        # 3. Llamamos al DAO estático
        DepartamentoDAO.actualizar_departamento(departamento_actualizado)

    """---------------------------------------------------------------------------------------------------------------------"""

    @staticmethod
    def eliminar_departamento(id_departamento: int):
        """
        Elimina un departamento por su ID.
        """
        if int(id_departamento) <= 0:
            print("Error: ID de departamento inválido.")
            return
            
        DepartamentoDAO.eliminar_departamento(int(id_departamento))

    """---------------------------------------------------------------------------------------------------------------------"""

    @staticmethod
    def obtener_departamento_por_id(id_departamento: int) -> Departamento:
        """
        Busca un departamento por su ID.
        Retorna un objeto Departamento o None.
        """
        if int(id_departamento) <= 0:
            print("Error: ID de departamento inválido.")
            return None
            
        return DepartamentoDAO.obtener_departamento_por_id(int(id_departamento))