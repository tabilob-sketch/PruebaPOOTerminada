# persistencia/departamentoDAO.py
from typing import List, Dict, Optional
from persistencia.conexion import Conexion
from dominio.departamento import Departamento

con = Conexion()

class DepartamentoDAO:
    """DAO para la tabla 'departamento'"""

    # ===== C =====
    @staticmethod
    def guardar_departamento(departamento: Departamento) -> None:
        sql = "INSERT INTO departamento (nombre, tipo_departamento) VALUES (%s, %s)"
        valores = (
            departamento.obtener_nombre(),
            departamento.obtener_tipo_departamento().value
        )
        cx = con.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, valores)
                cx.commit()
                print("SE HA INSERTADO CORRECTAMENTE")
        except Exception as e:
            cx.rollback()
            print(f"Error al insertar departamento: {e}")
            raise
        finally:
            con.cerrar_conexion(cx)

    # ===== R (por ID) =====
    @staticmethod
    def obtener_departamento_por_id(id_departamento: int) -> Optional[Dict]:
        sql = """
        SELECT id_departamento, nombre, tipo_departamento
        FROM departamento
        WHERE id_departamento = %s
        """
        cx = con.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, (id_departamento,))
                return cur.fetchone()
        finally:
            con.cerrar_conexion(cx)

    # ===== R (listar todos) =====
    @staticmethod
    def listar_departamentos() -> List[Dict]:
        sql = """
        SELECT id_departamento, nombre, tipo_departamento
        FROM departamento
        ORDER BY nombre
        """
        cx = con.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
        finally:
            con.cerrar_conexion(cx)

    # ===== R (buscar por nombre) =====
    @staticmethod
    def buscar_departamentos_por_nombre(nombre: str) -> List[Dict]:
        sql = """
        SELECT id_departamento, nombre, tipo_departamento
        FROM departamento
        WHERE UPPER(nombre) LIKE UPPER(%s)
        ORDER BY nombre
        """
        patron = f"%{(nombre or '').strip()}%"
        cx = con.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, (patron,))
                return cur.fetchall()
        finally:
            con.cerrar_conexion(cx)

    # ===== U =====
    @staticmethod
    def actualizar_departamento(departamento: Departamento) -> None:
        sql = "UPDATE departamento SET nombre = %s, tipo_departamento = %s WHERE id_departamento = %s"
        valores = (
            departamento.obtener_nombre(),
            departamento.obtener_tipo_departamento().value,
            departamento.obtener_id_departamento()
        )
        cx = con.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, valores)
                cx.commit()
                print("SE HA ACTUALIZADO CORRECTAMENTE")
        except Exception as e:
            cx.rollback()
            print(f"Error al actualizar departamento: {e}")
            raise
        finally:
            con.cerrar_conexion(cx)

    # ===== D =====
    @staticmethod
    def eliminar_departamento(id_departamento: int) -> None:
        sql = "DELETE FROM departamento WHERE id_departamento = %s"
        cx = con.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, (id_departamento,))
            cx.commit()
            print(f"SE HA ELIMINADO EL DEPARTAMENTO CON EL ID: {id_departamento}")
        except Exception as e:
            cx.rollback()
            print(f"Error al eliminar departamento: {e}")
            raise
        finally:
            con.cerrar_conexion(cx)
