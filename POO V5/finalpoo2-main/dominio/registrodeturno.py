"""Dentro de este archivo se encontrara la clase registrodeturno"""
import datetime

class RegistroDeTurno:
    def __init__(self,id_registro: int, fecha: datetime, cantidad_horas: int, tareas_realizadas: str) -> None:
        """Esta clase permite registrar objetos de la clase RegistroDeTurno
        Parametros:
            id_registro -> corresponde al id de cada registro
            fecha: datatime -> corresponde a la fecha que se registro el turno
            cantidad_horas: int -> corresponde a la cantidad de horas del turno
            tareas_realizadas: str -> corresponde a las tareas realizadas durante el turno
        Retorno:
            No contiene retorno 
        """
        self.id_registro = id_registro
        self.fecha = fecha
        self.cantidad_horas = cantidad_horas
        self.tareas_realizadas = tareas_realizadas

        def __str__(self) -> str:
            return f" Fecha del turno: {self.fecha}, Cantidad de horas: {self.cantidad_horas}, Tarea realizada: {self.tareas_realizadas}"
        
    def obtener_id_registro(self):
        return self.id_registro

    def obtener_id_empleado(self):
        return self.id_empleado

    def obtener_fecha(self):
        return self.fecha
    
    def obtener_cantidad_horas(self):
        return self.cantidad_horas
    
    def obtener_tareas_realizadas(self):
        return self.tareas_realizadas
    
        