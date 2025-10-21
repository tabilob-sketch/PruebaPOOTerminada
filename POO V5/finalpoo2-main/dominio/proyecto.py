"""Dentro de este archivo se encontrara la clase proyecto"""
import datetime
from dominio.empleado import Empleado 

class Proyecto:
    def __init__(self, id_proyecto: int , nombre: str, descripcion: str, fecha_inicio: datetime) -> None:
        """Esta clase permite crear objetos de la clase Proyecto
        Paramentros:
            id_proyecto: int -> Corresponde al ID del proyecto
            nombre: str -> corresponde al nombre del proyecto
            descripcion: str -> corresponde a la descripcion del proyecto
            fecha_inicio: datetime -> corresponde a la fecha de inicio del proyecto
        Retorno:
            No contiene retorno
        """
        self.id_proyecto = id_proyecto # ¡AGREGADO EL ATRIBUTO ID!
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.empleado_asginados = [] #Aqui relacionamos a los empleados con el proyecto

    # MÉTODO ESPECIAL (CORRECCIÓN DE IDENTACIÓN)
    def __str__(self) -> str:
        return f"ID: {self.id_proyecto}, Nombre del proyecto: {self.nombre}, Descripcion: {self.descripcion}, Fecha de inicio: {self.fecha_inicio}"
        
    # MÉTODOS GETTERS 
    def obtener_id(self) -> int:
        return self.id_proyecto

    def obtener_nombre(self) -> str:
        return self.nombre

    def obtener_descripcion(self) -> str:
        return self.descripcion

    def obtener_fecha_inicio(self) -> datetime:
        return self.fecha_inicio
    
    # MÉTODOS SETTERS (ÚTIL PARA ESTABLECER EL ID DESPUÉS DE LA INSERCIÓN EN BD)
    def establecer_id(self, id_proyecto: int) -> None:
        self.id_proyecto = id_proyecto

    # METODO CREAR PROYECTO
    def nuevoProyecto(self):
        print(f"Proyecto: {self.nombre}: Ha sido creado exitosamente")

    # METODO EDITAR PROYECTO
    def editarProyecto(self, nuevo_nombre: str = None, nueva_descripcion: str = None):
        if nuevo_nombre:
            self.nombre = nuevo_nombre
        if nueva_descripcion:
            self.descripcion = nueva_descripcion
        print(f"Proyecto {self.nombre} Actualizado")

    # METODO ELIMINAR PROYECTO
    def eliminarProyecto(self):
        print(f"Proyecto: {self.nombre} Eliminado exitosamente")
        
    # METODO ASIGNAR EMPLEADO
    def asignarEmpledo(self, empleado: Empleado):
        if empleado not in self.empleado_asginados:
            self.empleado_asginados.append(empleado)
            print(f"Empleado: {empleado.nombre} Asignado correctamente al proyecto")
        else:
            print(f"Empleado: {empleado.nombre} Ya esta asignado a un proyecto")

    # METODO DESASIGNAR EMPLEADO
    def desaginarEmpledo(self, empleado: Empleado):
        if empleado in self.empleado_asginados:
            self.empleado_asginados.remove(empleado)
            print(f"Empleado: {empleado.nombre} Eliminado correcatemente")
        else:
            print(f"Empleado: {empleado.nombre} Empleado no asignado en el Proyecto")