# persistencia/departamentoDAO.py
# ==============================================================
# DAO (Data Access Object) de Departamento
# --------------------------------------------------------------
# - Encapsula TODO el acceso a la tabla `departamento`.
# - Ofrece métodos CRUD (Create/Read/Update/Delete).
# - Maneja conexiones, transacciones (commit/rollback) y cursores.
# - Devuelve filas como diccionarios (gracias a DictCursor en Conexion).
# ==============================================================

from typing import List, Dict, Optional
from persistencia.conexion import Conexion
from dominio.departamento import Departamento

# Instancia reutilizable para obtener/cerrar conexiones
con = Conexion()

class DepartamentoDAO:
    """DAO para la tabla 'departamento'."""

    # ============================= C (CREATE) =============================
    @staticmethod
    def guardar_departamento(departamento: Departamento) -> None:
        """
        Inserta un nuevo departamento en la BD.
        Recibe un objeto de dominio `Departamento` y toma:
          - nombre (str)
          - tipo_departamento (Enum) -> se guarda su .value (texto)
        """
        sql = """
            INSERT INTO departamento (nombre, tipo_departamento)
            VALUES (%s, %s)
        """
        valores = (
            departamento.obtener_nombre(),
            departamento.obtener_tipo_departamento().value  # guardamos el texto del Enum
        )

        cx = con.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, valores)
                cx.commit()   # confirmamos la transacción
                print("SE HA INSERTADO CORRECTAMENTE")
        except Exception as e:
            cx.rollback()    # deshacemos cambios si algo falla
            print(f"Error al insertar departamento: {e}")
            raise           # re-lanzamos para que la capa superior decida
        finally:
            con.cerrar_conexion(cx)

    # ===================== R (READ: obtener por ID) ======================
    @staticmethod
    def obtener_departamento_por_id(id_departamento: int) -> Optional[Dict]:
        """
        Obtiene un departamento por su ID.
        Retorna:
          - dict con {id_departamento, nombre, tipo_departamento} si existe.
          - None si no hay coincidencia.
        """
        sql = """
            SELECT id_departamento, nombre, tipo_departamento
            FROM departamento
            WHERE id_departamento = %s
        """
        cx = con.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, (id_departamento,))
                return cur.fetchone()  # una fila o None
        finally:
            con.cerrar_conexion(cx)

    # ===================== R (READ: listar todos) ========================
    @staticmethod
    def listar_departamentos() -> List[Dict]:
        """
        Lista todos los departamentos, ordenados por nombre.
        Retorna una lista de dicts.
        """
        sql = """
            SELECT id_departamento, nombre, tipo_departamento
            FROM departamento
            ORDER BY nombre
        """
        cx = con.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()  # lista de dicts
        finally:
            con.cerrar_conexion(cx)

    # ================= R (READ: buscar por nombre LIKE) ==================
    @staticmethod
    def buscar_departamentos_por_nombre(nombre: str) -> List[Dict]:
        """
        Busca departamentos cuyo nombre contenga el texto dado (LIKE %texto%).
        Comparación case-insensitive usando UPPER().
        """
        sql = """
            SELECT id_departamento, nombre, tipo_departamento
            FROM departamento
            WHERE UPPER(nombre) LIKE UPPER(%s)
            ORDER BY nombre
        """
        patron = f"%{(nombre or '').strip()}%"  # normalizamos entrada
        cx = con.obtener_conexion()
        try:
            with cx.cursor() as cur:
                cur.execute(sql, (patron,))
                return cur.fetchall()
        finally:
            con.cerrar_conexion(cx)

    # ============================= U (UPDATE) ============================
    @staticmethod
    def actualizar_departamento(departamento: Departamento) -> None:
        """
        Actualiza nombre y tipo_departamento de un registro existente.
        Recibe un objeto `Departamento` con:
          - id_departamento (int)  -> PK existente
          - nombre (str)
          - tipo_departamento (Enum) -> se guarda su .value (texto)
        """
        sql = """
            UPDATE departamento
            SET nombre = %s, tipo_departamento = %s
            WHERE id_departamento = %s
        """
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

    # ============================= D (DELETE) ============================
    @staticmethod
    def eliminar_departamento(id_departamento: int) -> None:
        """
        Elimina físicamente un departamento por su ID.
        Nota: eliminación física borra el registro definitivamente.
              Si necesitas auditoría/histórico, considera eliminación lógica.
        """
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
