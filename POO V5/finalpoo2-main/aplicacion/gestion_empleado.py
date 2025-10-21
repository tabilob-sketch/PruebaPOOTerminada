from dominio.empleado import Empleado
from persistencia.empleadoDAO import empleadoDAO
from datetime import datetime

class gestionempleado():
    @staticmethod
    def crear_empleado(nombre, direccion, numero_telefono, correo_electronico, fecha_inicio_contrato, salario, usuario, tipo_empleado):
        tipo_enum = Empleado.TipoEmpleado(tipo_empleado) #Convertimos el str a Enum
        empleado = Empleado(None, nombre, direccion, numero_telefono, correo_electronico, fecha_inicio_contrato, salario, usuario,tipo_enum)
        empleadoDAO.nuevo_empleado(empleado)
    
    @staticmethod
    def eliminar_empleado(id_empleado):
        empleadoDAO.eliminar_empleado(id_empleado)
    
    @staticmethod
    def buscar_empleado(id_empleado):
        empleadoDAO.buscar_empleado(id_empleado)

    @staticmethod
    def editar_empleado(id_empleado: int, nombre: str, direccion: str, telefono: int, correo: str, fecha_inicio: datetime, salario: int, usuario: str, tipo_empleado: str):
        tipo_enum = Empleado.TipoEmpleado(tipo_empleado)
        empleadoDAO.editar_empleado(nombre, direccion, telefono, correo, fecha_inicio, salario, usuario, tipo_enum.value, id_empleado)
