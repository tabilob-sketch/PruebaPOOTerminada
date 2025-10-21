from persistencia.conexion import Conexion  #Desde la capa de persistencia dentro del archivo conexion importamos la clase Conexion
from dominio.proyecto import Proyecto

#creamos la instancia de conexion
con = Conexion() #Llamamos a la clase Conexion

#creamos la clase ProyectoDAO

class ProyectoDAO:
    """
    DAO es una clase la cual podemos manipular los datos para realizar diferentes operaciones.
    """
    @staticmethod #aqui definimos un metodo dentro de una clase que no depende de una instancia "No usamos self"
    def guardar_proyecto(proyecto:Proyecto):
        """
        Aqui vamos a guardar un proyecto dentro de la base de datos

        Parametros:
        proyecto -> Instancia de clase Proyecto 

        """
        #Hacemos la consulta a la BD
        query = "INSERT INTO PROYECTO (nombre, descripcion, fecha_inicio) VALUES (%s, %s , %s)" #Hacemos la insersion de los dato
        valores = ( #definimos una tupla para que los valores no cambien ni muten que contendra los datos insertados en la BD
            proyecto.obtener_nombre(), #Obtenemos el valor del nombre -> VARCHAR
            proyecto.obtener_descripcion(), #Obtenemos el valor de la descripcion -> TEXT
            proyecto.obtener_fecha_inicio(), #Obtenemos el valor de la fecha de inicio del proyecto -> DATETIME
        )
        conexion = con.obtener_conexion() #Aqui establecemos o recuperamos una conexion ACTIVA  
        try:
            with conexion.cursor() as cursor: #Con cursor podemos ejecutar el comando o comandos SQL
                cursor.execute(query, valores) #Ejecutamos la consulta "query" 
                conexion.commit() #Guardamos y confirmamos los cambios
                print("SE HA INSERTADO CORRECTAMENTE")
        except Exception as e:
            print(f"Ocurrio un al INSERTAR un proyecto: {e}")
        finally:
            con.cerrar_conexion(conexion)
    "---------------------------------------------------------------------------------------------------------------------"
    """
    
    Aqui vamos a buscar un proyecto por su id dentro de la base de datos
    
    Parametros:
        id: ID del proyecto en la base de datos
    Retorno:
        Diccionario con los datos del proyecto  
    """
    @staticmethod
    def obtener_proyecto_por_id(id_proyecto): 
    
    #Hacemos la consutla a la BD
        query = "SELECT * FROM PROYECTO WHERE id_proyecto = %s" #Hacemos la consulta para hacer la seleccion del id de un proyecto
        conexion = con.obtener_conexion() #Aqui establecemos o recuperamos una conexion ACTIVA 
        try: 
            with conexion.cursor() as cursor:
                cursor.execute()(query, (id_proyecto,))
                return cursor.fetchone() #Aqui llamamos a que solamente traiga el id del proyecto, fetchone solamente trae una fila dentro de los campos de la tabla
            print("SE HA OBTENIDO EL PROYECTO")
        except Exception as e:
            print(f"Ocurrio un error al SELECCIONAR el ID: {e}")
            return None
        finally:
            con.cerrar_conexion(conexion) #CERRAMOS LA CONEXION  A LA BD
    "---------------------------------------------------------------------------------------------------------------------"
    """

    Aqui vamos a eliminar un proyecto por su id dentro de la base de datos

    Parametros:
        id_proyecto: ID de proyecto para eliminar
    Retorno:
        No vamos a retornar nada ya que buscamo eliminar un proyecto
    """

    @staticmethod
    def eliminar_proyecto(id_proyecto):

    #Hacemos la consulta a la BD
        query = "DELETE FROM PROYECTO WHERE id_proyecto = %s" #Hacemos la consulta para hacer la eliminacion de un proyecto
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (id_proyecto,)) #ejecutamos la query y el id_proyecto
            conexion.commit() #Guardamos y confirmamos los cambios
            print(f"SE HA ELIMINADO EL PROYECTO CON EL ID: {id_proyecto}")
        except Exception as e:
            print(f"Error al ELIMINAR un proyecto: {e}")
        finally:
            con.cerrar_conexion(conexion)
    "---------------------------------------------------------------------------------------------------------------------"
    """
    Aqui vamos actualizar un proyecto su nombre, descripcion y fecha de inicio

    Parametros
        id_proyecto = el ID de cada departamento
        nombre = nombre del departamento
        tipo_departamento = el tipo de cada departamento    
    """

    @staticmethod
    def actualizar_proyecto(nombre, descripcion,fecha_inicio, id_proyecto):
        query = "UPDATE PROYECTO SET nombre = %s, descripcion = %s, fecha_inicio = %s WHERE id_proyecto = %s"
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (nombre, descripcion, fecha_inicio, id_proyecto))
                conexion.commit()
                print("SE HA ACTUALIZADO CORRECTAMENTE")
        except Exception as e:
            print(f"ERROR AL REALIZAR CAMBIOS: {e}")
        finally:
            con.cerrar_conexion(conexion)
