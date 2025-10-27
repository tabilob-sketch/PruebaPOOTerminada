# persistencia/proyectoDAO.py
from typing import List, Dict, Optional
from datetime import datetime, date
from persistencia.conexion import Conexion  # Desde la capa de persistencia
from dominio.proyecto import Proyecto

# Instancia de conexión
con = Conexion()

def _to_datetime(v):
    if isinstance(v, datetime):
        return v
    if isinstance(v, date):
        return datetime.combine(v, datetime.min.time())
    return v

class ProyectoDAO:
    """
    DAO para la tabla PROYECTO.
    Columnas asumidas: id_proyecto, nombre, descripcion, fecha_inicio
    (Si tienes más campos, me dices y lo ajustamos).
    """

    # ---------------- C: Crear ----------------
    @staticmethod
    def guardar_proyecto(proyecto: Proyecto):
        """Inserta un proyecto en la BD."""
        query = """
            INSERT INTO PROYECTO (nombre, descripcion, fecha_inicio)
            VALUES (%s, %s, %s)
        """
        valores = (
            proyecto.obtener_nombre(),
            proyecto.obtener_descripcion(),
            proyecto.obtener_fecha_inicio(),  # datetime o date
        )
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, valores)
            conexion.commit()
            print("SE HA INSERTADO CORRECTAMENTE")
        except Exception as e:
            print(f"Ocurrió un error al INSERTAR un proyecto: {e}")
        finally:
            con.cerrar_conexion(conexion)

    # ---------------- R: Leer (detalle por ID) ----------------
    @staticmethod
    def obtener_proyecto_por_id(id_proyecto: int) -> Optional[Dict]:
        """Retorna un dict con los datos del proyecto o None si no existe."""
        query = "SELECT id_proyecto, nombre, descripcion, fecha_inicio FROM PROYECTO WHERE id_proyecto = %s"
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (id_proyecto,))
                r = cursor.fetchone()
                if not r:
                    return None
                return {
                    "id_proyecto": r["id_proyecto"],
                    "nombre": r["nombre"],
                    "descripcion": r["descripcion"],
                    "fecha_inicio": _to_datetime(r["fecha_inicio"]),
                }
        except Exception as e:
            print(f"Ocurrió un error al SELECCIONAR por ID: {e}")
            return None
        finally:
            con.cerrar_conexion(conexion)

    # ---------------- U: Actualizar ----------------
    @staticmethod
    def actualizar_proyecto(nombre: str, descripcion: str, fecha_inicio, id_proyecto: int):
        """Actualiza nombre, descripción y fecha_inicio por ID."""
        query = """
            UPDATE PROYECTO
            SET nombre = %s, descripcion = %s, fecha_inicio = %s
            WHERE id_proyecto = %s
        """
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

    # ---------------- D: Eliminar ----------------
    @staticmethod
    def eliminar_proyecto(id_proyecto: int):
        """Eliminación FÍSICA del proyecto por ID."""
        query = "DELETE FROM PROYECTO WHERE id_proyecto = %s"
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (id_proyecto,))
            conexion.commit()
            print(f"SE HA ELIMINADO EL PROYECTO CON EL ID: {id_proyecto}")
        except Exception as e:
            print(f"Error al ELIMINAR un proyecto: {e}")
        finally:
            con.cerrar_conexion(conexion)

    # ============== NUEVOS ==============

    @staticmethod
    def listar_proyectos() -> List[Dict]:
        """Lista todos los proyectos."""
        query = "SELECT id_proyecto, nombre, descripcion, fecha_inicio FROM PROYECTO ORDER BY nombre"
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                out: List[Dict] = []
                for r in rows:
                    out.append({
                        "id_proyecto": r["id_proyecto"],
                        "nombre": r["nombre"],
                        "descripcion": r["descripcion"],
                        "fecha_inicio": _to_datetime(r["fecha_inicio"]),
                    })
                return out
        except Exception as e:
            print(f"Error al LISTAR proyectos: {e}")
            return []
        finally:
            con.cerrar_conexion(conexion)

    @staticmethod
    def buscar_proyectos_por_nombre(texto: str) -> List[Dict]:
        """Busca proyectos por nombre usando LIKE."""
        query = """
            SELECT id_proyecto, nombre, descripcion, fecha_inicio
            FROM PROYECTO
            WHERE nombre LIKE %s
            ORDER BY nombre
        """
        conexion = con.obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (f"%{texto.strip()}%",))
                rows = cursor.fetchall()
                out: List[Dict] = []
                for r in rows:
                    out.append({
                        "id_proyecto": r["id_proyecto"],
                        "nombre": r["nombre"],
                        "descripcion": r["descripcion"],
                        "fecha_inicio": _to_datetime(r["fecha_inicio"]),
                    })
                return out
        except Exception as e:
            print(f"Error al BUSCAR proyectos por nombre: {e}")
            return []
        finally:
            con.cerrar_conexion(conexion)
