# aplicacion/gestionproyecto.py
# ==============================================================
# CAPA DE APLICACIÓN PARA PROYECTOS
# --------------------------------------------------------------
# Esta capa se encarga de:
#   - Recibir datos desde la presentación (menús/inputs).
#   - Crear/editar/eliminar proyectos a través del DAO.
#   - (Opcional) Validar/normalizar entradas antes de tocar la BD.
#
# Beneficios:
#   * Separa la UI (menús) de la lógica y del acceso a datos.
#   * Hace el código más mantenible y testeable.
# ==============================================================

from dominio.proyecto import Proyecto            # Modelo de dominio (clase Proyecto)
from persistencia.proyectoDAO import ProyectoDAO # Acceso a datos (consultas SQL)

class gestionProyecto:
    """
    Clase “servicio” (sin estado) que orquesta las operaciones sobre Proyectos.
    Conecta la clase de dominio (Proyecto) con el DAO (ProyectoDAO).
    """

    # ===================== C  (CREATE) =====================
    @staticmethod
    def crear_proyecto(nombre, descripcion, fecha_inicio):
        """
        Crea un nuevo Proyecto.

        Parámetros:
            nombre        : str   -> Nombre del proyecto (ej. "Sistema X")
            descripcion   : str   -> Descripción del proyecto
            fecha_inicio  : date/datetime/str -> Fecha de inicio; el DAO/BD deben aceptar su formato

        Flujo:
            1) Construye un objeto de dominio Proyecto (id=None porque la BD lo autogenera).
            2) Ejecuta lógica del dominio (si tu clase Proyecto define 'nuevoProyecto()', se invoca aquí).
            3) Delegamos el INSERT al DAO para persistir en la BD.
            4) Retornamos el objeto por si la UI quiere mostrarlo.

        Retorna:
            Proyecto (instancia recién creada; OJO: no trae el id salvo que lo setees en el DAO)
        """
        # 1) Construimos el objeto de dominio. La PK (id_proyecto) la generará la BD.
        proyecto = Proyecto(None, nombre, descripcion, fecha_inicio)

        # 2) Lógica de dominio: si la clase Proyecto define trabajo extra al "nacer", lo ejecutamos.
        #    (Si tu método 'nuevoProyecto' no hace nada o no existe, puedes omitir esta línea)
        proyecto.nuevoProyecto()

        # 3) Persistimos en BD a través del DAO (INSERT).
        ProyectoDAO.guardar_proyecto(proyecto)

        # 4) Devolvemos el objeto (útil para mostrar datos o continuar flujo).
        return proyecto

    # ===================== U  (UPDATE) =====================
    @staticmethod
    def editar_proyecto(id_proyecto, nombre, descripcion, fecha_inicio):
        """
        Actualiza un Proyecto existente en la BD.

        Parámetros:
            id_proyecto   : int   -> ID del proyecto a editar
            nombre        : str   -> Nuevo nombre
            descripcion   : str   -> Nueva descripción
            fecha_inicio  : date/datetime/str -> Nueva fecha de inicio

        Nota:
            Aquí delegamos la actualización al DAO. Si quisieras validaciones
            (p. ej., nombre con largo mínimo, fecha válida), este es un buen lugar.
        """
        ProyectoDAO.actualizar_proyecto(nombre, descripcion, fecha_inicio, id_proyecto)

    # ===================== D  (DELETE) =====================
    @staticmethod
    def eliminar_proyecto(id_proyecto):
        """
        Elimina físicamente (DELETE) un Proyecto por su ID.

        Parámetros:
            id_proyecto   : int -> ID a eliminar

        Nota:
            Eliminación física = el registro desaparece de la BD.
            Si prefieres “eliminación lógica”, cambia la estrategia en el DAO.
        """
        ProyectoDAO.eliminar_proyecto(id_proyecto)

    # ===================== R  (READ: listar todos) =====================
    @staticmethod
    def listar_todos():
        """
        Devuelve una lista con todos los proyectos.

        Retorna:
            List[Dict]: cada elemento típicamente con:
                {
                  'id_proyecto': int,
                  'nombre': str,
                  'descripcion': str,
                  'fecha_inicio': date/datetime
                }
            (El formato exacto depende de lo que construye el DAO.)
        """
        return ProyectoDAO.listar_proyectos()

    # ===================== R  (READ: buscar por nombre) =====================
    @staticmethod
    def buscar_por_nombre(texto: str):
        """
        Busca proyectos por coincidencia en el nombre (LIKE %texto%).

        Parámetros:
            texto : str -> parte del nombre a buscar (case-insensitive si el DAO lo aplica)

        Retorna:
            List[Dict] con la misma estructura que listar_todos(), pero filtrada.
        """
        return ProyectoDAO.buscar_proyectos_por_nombre(texto)
