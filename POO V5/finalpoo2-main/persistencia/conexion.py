"""Aqui encontraras la conexion a la BD local"""

#Importacion del modulo pymysql

import pymysql
import pymysql.cursors # Necesario para usar DictCursor

class Conexion:
    """
    Con esta clase administramos la conexion a la base de datos
    - Definimos los parametros de conexion
    - Definimos las credenciales de la BD en un archivo seguro
    """

    def __init__(self): #self nos sirve para hacer mencion en una misma clase
        self.host       = "localhost" 
        self.user       = "root"
        self.password   = "admin"
        self.base_datos = "bdpoo"

    def obtener_conexion(self):
        """Establemos la conexion a la BD con una devolucion de la BD"""
        try:
            conexion = pymysql.Connect(
                host        = self.host,       # establecemos al lugar o host que se va a establecer la conexion
                user        = self.user,       # establecemos con el usuario que se va a conectar a la bd
                password    = self.password,   # establecemos la contraseña que se necesitara para ingresar a la bd
                database    = self.base_datos, # establecemos a la bd que se va a conectar
                
                # Cursorclass configura el cursor para que sean diccionarios de clave-valor
                cursorclass = pymysql.cursors.DictCursor
            )
            # CORRECCIÓN 2: Se debe retornar la INSTANCIA de conexión 'conexion', no la CLASE 'Conexion'
            return conexion 
        except pymysql.MySQLError as e:
            print(f"ERROR AL HACER LA CONEXION: {e}")
            raise # enviamos el error a un superior 

    def cerrar_conexion(self, conexion): #self nos sirve para hacer mencion en una misma clase
        """Aqui si tenemos una conexion activa haremos cierre de la misma conexion"""
        if conexion: #Si existe conexion
            conexion.close()