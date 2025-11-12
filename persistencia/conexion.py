# persistencia/conexion.py
# ==============================================================
# CONEXIÓN A BD (MySQL/MariaDB) con PyMySQL
# Lee credenciales desde .env vía aplicacion.config
# ==============================================================

import pymysql
import pymysql.cursors
from aplicacion import config

class Conexion:
    """
    Administra la conexión a la BD usando credenciales del .env.
    Entrega cursor tipo diccionario (DictCursor).
    """

    def __init__(self):
        self.host       = config.DB_HOST
        self.user       = config.DB_USER
        self.password   = config.DB_PASSWORD
        self.base_datos = config.DB_NAME
        self.port       = config.DB_PORT

    def obtener_conexion(self):
        try:
            conexion = pymysql.Connect(
                host        = self.host,
                user        = self.user,
                password    = self.password,
                database    = self.base_datos,
                port        = self.port,
                charset     = "utf8mb4",
                cursorclass = pymysql.cursors.DictCursor
            )
            return conexion
        except pymysql.MySQLError as e:
            print(f"ERROR AL CONECTAR A LA BD: {e}")
            raise

    def cerrar_conexion(self, conexion):
        try:
            if conexion:
                conexion.close()
        except Exception:
            pass
