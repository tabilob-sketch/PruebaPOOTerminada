# persistencia/conexion.py
# ==============================================================
# CONEXIÓN A BASE DE DATOS (MySQL/MariaDB) CON PyMySQL
# --------------------------------------------------------------
# - Centraliza la configuración de conexión.
# - Entrega conexiones con cursor tipo diccionario (DictCursor).
# - Expone métodos simples: obtener_conexion() / cerrar_conexion().
#
# Nota: en producción, es recomendable mover credenciales a un .env
# ==============================================================

import pymysql
import pymysql.cursors  # Para usar DictCursor (row -> dict)

class Conexion:
    """
    Administra la conexión a la base de datos.
    Responsabilidades:
      - Guardar parámetros de conexión (host, user, pass, db, etc.)
      - Entregar una conexión abierta con cursor tipo diccionario.
      - Cerrar conexiones activas de forma segura.

    Uso típico (DAO):
        con = Conexion().obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute("SELECT 1")
                rows = cur.fetchall()
            con.commit()     # si hubo INSERT/UPDATE/DELETE
        except Exception:
            con.rollback()   # ante errores en operaciones de escritura
            raise
        finally:
            Conexion().cerrar_conexion(con)
    """

    def __init__(self):
        """
        Define parámetros de conexión.
        Sugerencia: en proyectos reales, lee estas variables desde .env
        para no hardcodear credenciales.
        """
        self.host       = "127.0.0.1"  # o "localhost"
        self.user       = "root"
        self.password   = ""
        self.base_datos = "bdpoo"
        self.port       = 3306         # puerto por defecto MySQL/MariaDB

    def obtener_conexion(self):
        """
        Abre y retorna una conexión activa a la BD.
        - cursorclass=DictCursor hace que fetchone/fetchall devuelvan dicts:
            r["columna"] en vez de r[0]
        - charset y autocommit se pueden ajustar según tu proyecto.
        """
        try:
            conexion = pymysql.Connect(
                host        = self.host,
                user        = self.user,
                password    = self.password,
                database    = self.base_datos,
                port        = self.port,
                charset     = "utf8mb4",                 # soporta emojis y tildes
                cursorclass = pymysql.cursors.DictCursor # filas como dict
                # autocommit=False por defecto -> usas commit()/rollback() manualmente
            )
            # Opcional: mantener viva la conexión en sesiones largas
            # conexion.ping(reconnect=True)
            return conexion
        except pymysql.MySQLError as e:
            # Captura errores específicos de MySQL/PyMySQL
            print(f"ERROR AL CONECTAR A LA BD: {e}")
            # Re-levanta la excepción para que el DAO decida qué hacer
            raise

    def cerrar_conexion(self, conexion):
        """
        Cierra la conexión si está abierta.
        Llamar siempre en un bloque finally para liberar recursos.
        """
        try:
            if conexion:
                conexion.close()
        except Exception:
            # En cierre, no queremos interrumpir el flujo si ya hay otra excepción en curso.
            pass
