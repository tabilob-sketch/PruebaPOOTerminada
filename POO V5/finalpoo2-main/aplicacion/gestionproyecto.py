#Dentro de la capa de aplicacion vamos a conectar las Clases con las consultasd de la BD
from dominio.proyecto import Proyecto
from persistencia.proyectoDAO import ProyectoDAO

class gestionProyecto():
    """
    Aqui vamos a gestionar los proyectos ya sea crear, editar, eliminar haciendo que la Clase se comunique con la BD

    Parametros:
        nombre = nombre de cada proyecto
        decripcion = descripcion de cada proyecto
        fecha_inicio = fecha de inicio de cada proyecto
    Retorno:
        proyecto = va a retonar un proyecto creado
    """
    @staticmethod
    def crear_proyecto(nombre, descripcion, fecha_inicio):
        proyecto = Proyecto(None, nombre, descripcion, fecha_inicio)
        proyecto.nuevoProyecto() #Metodo de proyecto
        ProyectoDAO.guardar_proyecto(proyecto)
        return proyecto #retornamos proyecto 
    """---------------------------------------------------------------------------------------------------------------------"""
    """
    Aqui vamos a vamos a editar un proyecto ya creado

    Parametros:
        id_proyecto = id de cada proyecto
        nombre = nombre de cada proyecto
        descripcion = descripcion de cada proyeto
    
    Retorno:
        No contiene retorno
    """
    @staticmethod
    def editar_proyecto(id_proyecto, nombre , descripcion, fecha_inicio):
        ProyectoDAO.actualizar_proyecto( nombre, descripcion,fecha_inicio, id_proyecto)
    """---------------------------------------------------------------------------------------------------------------------"""
    """
    Aqui vamos a eliminar un proyecto

    Parametros:
        id_proyecto = id de cada proyecto
    
    Retorno:
        No contiene retorno
    """

    @staticmethod
    def eliminar_proyecto(id_proyecto):
        ProyectoDAO.eliminar_proyecto(id_proyecto)