# persistencia/usuarioDAO.py
# ==============================================================
# DAO (Data Access Object) para la entidad Usuario
# Maneja todas las operaciones CRUD hacia la base de datos
# ==============================================================

from dominio.usuario import Usuario
from persistencia.conexion import Conexion
from pymysql.err import IntegrityError
from aplicacion.errores import DuplicadoError


class UsuarioDAO:
    def __init__(self):
        self.conexion = Conexion()

    def crear(self, usuario: Usuario) -> int:
        sql = """
            INSERT INTO usuarios (username, password_hash, nombre_completo, rol, activo)
            VALUES (%s, %s, %s, %s, %s)
        """
        cx = self.conexion.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, (
                    usuario.username,
                    usuario.password_hash,
                    usuario.nombre_completo,
                    usuario.rol,
                    int(bool(usuario.activo))
                ))
                cx.commit()
                return cur.lastrowid
        except IntegrityError as e:
            cx.rollback()
            # 1062 = duplicate key
            if getattr(e, "args", [None])[0] == 1062:
                raise DuplicadoError("username", usuario.username)
            raise
        except Exception as e:
            cx.rollback()
            print(f"Error al crear usuario: {e}")
            raise
        finally:
            self.conexion.cerrar_conexion(cx)

    def modificar(self, usuario: Usuario) -> bool:
        sql = """
            UPDATE usuarios
            SET username = %s,
                password_hash = %s,
                nombre_completo = %s,
                rol = %s,
                activo = %s
            WHERE id = %s
        """
        cx = self.conexion.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, (
                    usuario.username,
                    usuario.password_hash,
                    usuario.nombre_completo,
                    usuario.rol,
                    int(bool(usuario.activo)),
                    usuario.id
                ))
                cx.commit()
                return cur.rowcount > 0
        except IntegrityError as e:
            cx.rollback()
            if getattr(e, "args", [None])[0] == 1062:
                raise DuplicadoError("username", usuario.username)
            raise
        except Exception as e:
            cx.rollback()
            print(f"Error al modificar usuario: {e}")
            raise
        finally:
            self.conexion.cerrar_conexion(cx)

    def eliminar(self, id_usuario: int) -> bool:
        sql = "DELETE FROM usuarios WHERE id = %s"
        cx = self.conexion.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, (id_usuario,))
                cx.commit()
                return cur.rowcount > 0
        except Exception as e:
            cx.rollback()
            print(f"Error al eliminar usuario: {e}")
            raise
        finally:
            self.conexion.cerrar_conexion(cx)

    def listar_todos(self):
        sql = "SELECT id, username, password_hash, nombre_completo, rol, activo FROM usuarios ORDER BY id"
        cx = self.conexion.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql)
                filas = cur.fetchall()
                return [
                    Usuario(
                        id=f["id"],
                        username=f["username"],
                        password_hash=f["password_hash"],
                        nombre_completo=f["nombre_completo"],
                        rol=f["rol"],
                        activo=f["activo"],
                    )
                    for f in filas
                ]
        finally:
            self.conexion.cerrar_conexion(cx)

    def obtener_por_username(self, username: str):
        sql = "SELECT * FROM usuarios WHERE username = %s"
        cx = self.conexion.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, (username,))
                f = cur.fetchone()
                if f:
                    return Usuario(
                        id=f["id"],
                        username=f["username"],
                        password_hash=f["password_hash"],
                        nombre_completo=f["nombre_completo"],
                        rol=f["rol"],
                        activo=f["activo"],
                    )
                return None
        finally:
            self.conexion.cerrar_conexion(cx)

    def buscar_por_id(self, id_usuario: int):
        sql = "SELECT * FROM usuarios WHERE id = %s"
        cx = self.conexion.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, (id_usuario,))
                f = cur.fetchone()
                if f:
                    return Usuario(
                        id=f["id"],
                        username=f["username"],
                        password_hash=f["password_hash"],
                        nombre_completo=f["nombre_completo"],
                        rol=f["rol"],
                        activo=f["activo"],
                    )
                return None
        finally:
            self.conexion.cerrar_conexion(cx)
