from persistencia.conexion import Conexion
from dominio.registrodeturno import RegistroDeTurno
from dominio.empleado import Empleado

con = Conexion()

class registroturnoDAO:
    @staticmethod
    def guardar_turno(empleado:Empleado, registro_turno: RegistroDeTurno):
        query = "INSERT INTO REGISTRODETURNO (id_empleado, fecha, cantidad_horas, tareas_realizadas) VALUES (%s, %s, %s, %s)"
        valores = (
            empleado.obtener_id(),
            registro_turno.obtener_fecha(),
            registro_turno.obtener_tareas_realizadas()
        )

        conexion =con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query,(valores))
                conexion.commit()
                print("Turno registrado correctamente")
        except Exception as e:
            print(f"ERROR AL REGISTRAR EL TURNO: {e}")
        finally:
            con.cerrar_conexion(conexion)

    def buscar_por_id(id_registro):
        query = "SELECT * FROM REGISTRODETURNO WHERE id_registro = %s"
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query,(id_registro,))
                return cursor.fetchone()
        except Exception as e:
            print(f"ERROR AL BUSCAR EL REGISTRO: {e}")
        finally:
            con.cerrar_conexion(conexion)
    
    def eliminar_turno(id_registro):
        query = "DELETE FROM REGISTRODETURNO WHERE id_registro = %s"
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (id_registro,))
                conexion.commit()
                print(f"REGISTRO DE TURNO CON EL ID {id_registro} ELIMINADO")
        except Exception as e:
            print(f"ERROR AL ELIMINAR EL TURNO: {e}")
        finally:
            con.cerrar_conexion(conexion)
    
    def editar_turno(fecha, cantidad_horas, tareas_realizadas,id_registro):
        query = "UPDATE REGISTRODETURNO SET fecha = %s, cantidad_horas = %s, tareas_realizadas = %s WHERE id_registro = %s"
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query,(fecha,cantidad_horas,tareas_realizadas,id_registro))
                conexion.commit()
                print("SE HA ACTUALIZADO CORRECTAMENTE")
        except Exception as e:
            print(f"ERRO AL REALIZAR CAMBIOS: {e}")
        finally:
            con.cerrar_conexion(conexion)


