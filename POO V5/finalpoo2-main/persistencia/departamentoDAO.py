from persistencia.conexion import Conexion
from dominio.departamento import Departamento

#creamos la instancia de conexion
con = Conexion() #Llamamos a la clase Conexion

#creamos la clase DepartamentoDao

class DepartamentoDAO:
    """
    DAO es una clase la cual podemos manipular los datos para realizar diferentes operaciones.
    """
    @staticmethod #aqui definimos un metodo dentro de una clase que no depende de una instancia "No usamos self"
    def guardar_departamento(departamento:Departamento):
        """
        Aqui vamos a guardar un departamento dentro de la base de datos

        Parametros:
        departamento -> Instancia de clase Departamento 

        """
        #Hacemos la consulta a la BD
        query = "INSERT INTO DEPARTAMENTO (nombre, tipo_departamento) VALUES (%s, %s)"
        valores = (
            departamento.obtener_nombre(),
            departamento.obtener_tipo_departamento().value #values nos sirve para guardar el str del Enum
        )
        conexion = con.obtener_conexion() #Aqui establecemos o recuperamos una conexion ACTIVA
        try:
            with conexion.cursor() as cursor: #Con cursor podemos ejecutar el comando o comandos SQL
                cursor.execute(query, valores) #Ejecutamos la consulta "query" 
                conexion.commit() #Guardamos y confirmamos los cambios
                print("SE HA INSERTADO CORRECTAMENTE")
        except Exception as e:
            print(f"Ocurrio un al INSERTAR un DEPARTAMENTO: {e}")
        finally:
            con.cerrar_conexion(conexion)
    "---------------------------------------------------------------------------------------------------------------------"

    """
    
    Aqui vamos a buscar un departamento por su id dentro de la base de datos
    
    Parametros:
        id: ID del departamento en la base de datos
    Retorno:
        Diccionario con los datos del departamento 
    """
    @staticmethod
    def obtener_departamento_por_id(id_departamento):
        """
        Busca un departamento por su ID.
        """
        query = "SELECT * FROM DEPARTAMENTO WHERE id_departamento = %s"
        conexion = con.obtener_conexion()
        try: 
            with conexion.cursor() as cursor:
                cursor.execute(query, (id_departamento,))
                
                resultado = cursor.fetchone()
                
                if resultado:
                    print("SE HA OBTENIDO EL DEPARTAMENTO")
                    
                return resultado
                
        except Exception as e:
            print(f"Ocurrio un error al SELECCIONAR el ID: {e}")
            return None
        finally:
            if conexion:
                con.cerrar_conexion(conexion)
    "---------------------------------------------------------------------------------------------------------------------"
    """

    Aqui vamos a eliminar un departamento por su id dentro de la base de datos

    Parametros:
        id_departamento: ID de proyecto para eliminar
    Retorno:
        No vamos a retornar nada ya que buscamos eliminar un proyecto
    """
    @staticmethod
    def eliminar_departamento(id_departamento):
        #Hacemos la consulta a la BD

        query = "DELETE FROM DEPARTAMENTO WHERE id_departamento = %s" #Hacemos la consulta para hacer la eliminacion de un proyecto
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (id_departamento)) #ejecutamos la query y el id_departamento
            conexion.commit() #Guardamos y confirmamos los cambios
            print(f"SE HA ELIMINADO EL PROYECTO CON EL ID: {id_departamento}")
        except Exception as e:
            print(f"Error al ELIMINAR un proyecto: {e}")
        finally:
            con.cerrar_conexion(conexion)
    "---------------------------------------------------------------------------------------------------------------------"
    def actualizar_departamento(departamento:Departamento):
        query = "UPDATE DEPARTAMENTO SET nombre = %s, tipo_departamento= %s WHERE id_departamento = %s"
        valores = (
            departamento.obtener_nombre(),
            departamento.obtener_tipo_departamento().value,
            departamento.obtener_id_departamento()

        )
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (valores))
                conexion.commit()
                print("SE HA ACTUALIZADO CORRECTAMENTE")
        except Exception as e:
            print(f"ERROR AL REALIZAR CAMBIOS: {e}")
        finally:
            con.cerrar_conexion(conexion)