from persistencia.conexion import Conexion
from dominio.empleado import Empleado


con = Conexion()

class empleadoDAO:
    @staticmethod
    def nuevo_empleado(empleado:Empleado):
        query = "INSERT INTO EMPLEADO (nombre, direccion, numero_telefono, correo_electronico, fecha_inicio_contrato, salario, usuario, tipo_empleado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        conexion = con.obtener_conexion()
        valores = ( 
            empleado.obtener_nombre(), 
            empleado.obtener_direccion(), 
            empleado.obtener_numero_telefono(),
            empleado.obtener_correo_electronico(),
            empleado.obtener_fecha_inicio_contrato(),
            empleado.obtener_salario(),
            empleado.obtener_usuario(),
            empleado.obtener_tipo_empleado()
        )
        try:
            with conexion.cursor() as cursor: 
                cursor.execute(query, valores) 
                conexion.commit() 
                print("NUEVO EMPLEADO CREADO CORRECTAMENTE")
        except Exception as e:
            print(f"ERROR. EL EMPLEADO NO HA PODIDO SER AGREGADO: {e}")
        finally:
            con.cerrar_conexion(conexion)

    @staticmethod
    def eliminar_empleado(id_empleado):
        query = query = "DELETE FROM EMPLEADO WHERE id_empleado = %s" 
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (id_empleado,)) 
            conexion.commit()
            print(f"SE HA ELIMINADO EL EMPLEADO {id_empleado}")
        except Exception as e:
            print(f"ERROR AL ELMINIAR EMPLEADO: {e}")
        finally:
            con.cerrar_conexion(conexion)
    

    @staticmethod
    def buscar_empleado(id_empleado):
        query = "SELECT * FROM EMPLEADO WHERE id_empleado = %s" #Hacemos la consulta para hacer la seleccion del id de un proyecto
        conexion = con.obtener_conexion() #Aqui establecemos o recuperamos una conexion ACTIVA 
        try: 
            with conexion.cursor() as cursor:
                cursor.execute(query, (id_empleado,))
            resultado = cursor.fetchone()
            print(f"SE HA OBTENIDO EL EMPLEADO CON EL ID: {id_empleado}")
            return resultado
        except Exception as e:
            print(f"Ocurrio un error al BUSCAR un empleado por su ID: {e}")
            return None
        finally:
            con.cerrar_conexion(conexion) #CERRAMOS LA CONEXION  A LA BD

    @staticmethod
    def editar_empleado(nombre, direccion, numero_telefono, correo_electronico, fecha_inicio_contrato, salario, usuario, tipo_empleado, id_empleado):
        query = "UPDATE EMPLEADO SET nombre = %s, direccion = %s, numero_de_telefono = %s, correo_electronico = %s, fecha_inicio_contrato = %s, salario = %s, usuario = %s, tipo_empleado = %s WHERE id_empleado = %s"
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (nombre, direccion,numero_telefono, correo_electronico, fecha_inicio_contrato, salario, usuario, tipo_empleado, id_empleado))
                conexion.commit()
                print("SE HA ACTUALIZADO CORRECTAMENTE EL EMPLEADO")
        except Exception as e:
            print(f"ERROR AL REALIZAR CAMBIOS EN EMPLEADO: {e}")
        finally:
            con.cerrar_conexion(conexion)