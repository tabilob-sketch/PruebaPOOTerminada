# persistencia/empleadoDAO.py
from typing import List, Dict, Optional
from datetime import datetime, date
from persistencia.conexion import Conexion
from dominio.empleado import Empleado

# ----------------- Helpers -----------------
def _to_datetime(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    return value  # podría venir None o str (según driver)

# ----------------- C (Create) -----------------
def insert_empleado(emp: Empleado) -> int:
    """
    Inserta un empleado y devuelve el ID generado.
    """
    sql = """
        INSERT INTO empleado
        (nombre, direccion, numero_telefono, correo_electronico,
         fecha_inicio_contrato, salario, usuario, tipo_empleado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    tel_txt = str(emp.numero_telefono) if emp.numero_telefono is not None else None
    fic = emp.fecha_inicio_contrato
    if isinstance(fic, date) and not isinstance(fic, datetime):
        fic = datetime.combine(fic, datetime.min.time())
    tipo_txt = emp.tipo_empleado.value if hasattr(emp.tipo_empleado, "value") else str(emp.tipo_empleado)

    con = Conexion().obtener_conexion()
    try:
        with con.cursor() as cur:
            cur.execute(sql, (
                emp.nombre.strip(),
                emp.direccion.strip(),
                tel_txt,
                emp.correo_electronico.strip(),
                fic,
                float(emp.salario),
                emp.usuario.strip(),
                tipo_txt
            ))
            new_id = cur.lastrowid
        con.commit()
        return new_id
    except Exception:
        con.rollback()
        raise
    finally:
        Conexion().cerrar_conexion(con)

# ----------------- R (Read) -----------------
def buscar_empleado_detalle_por_id(id_empleado: int) -> Optional[Dict]:
    sql = """
    SELECT id_empleado, nombre, direccion, numero_telefono, correo_electronico,
           fecha_inicio_contrato, salario, usuario, tipo_empleado
    FROM empleado
    WHERE id_empleado=%s
    """
    con = Conexion().obtener_conexion()
    try:
        with con.cursor() as cur:
            cur.execute(sql, (id_empleado,))
            r = cur.fetchone()
            if not r:
                return None
            return {
                "id_empleado": r["id_empleado"],
                "nombre": r["nombre"],
                "direccion": r["direccion"],
                "correo": r["correo_electronico"],
                "telefono": r["numero_telefono"],
                "tipoempleado": r["tipo_empleado"],
                "fecha_inicio_contrato": _to_datetime(r["fecha_inicio_contrato"]),
                "salario": float(r["salario"]),
                "usuario": r["usuario"],
            }
    finally:
        Conexion().cerrar_conexion(con)

def listar_empleados() -> List[Dict]:
    sql = """
    SELECT id_empleado, nombre, direccion, numero_telefono, correo_electronico,
           fecha_inicio_contrato, salario, usuario, tipo_empleado
    FROM empleado
    ORDER BY nombre
    """
    con = Conexion().obtener_conexion()
    try:
        with con.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            out: List[Dict] = []
            for r in rows:
                out.append({
                    "id_empleado": r["id_empleado"],
                    "nombre": r["nombre"],
                    "direccion": r["direccion"],
                    "correo": r["correo_electronico"],
                    "telefono": r["numero_telefono"],
                    "tipoempleado": r["tipo_empleado"],
                    "fecha_inicio_contrato": _to_datetime(r["fecha_inicio_contrato"]),
                    "salario": float(r["salario"]),
                    "usuario": r["usuario"],
                })
            return out
    finally:
        Conexion().cerrar_conexion(con)

def buscar_empleados_por_nombre(texto: str) -> List[Dict]:
    sql = """
    SELECT id_empleado, nombre, direccion, numero_telefono, correo_electronico,
           fecha_inicio_contrato, salario, usuario, tipo_empleado
    FROM empleado
    WHERE nombre LIKE %s
    ORDER BY nombre
    """
    con = Conexion().obtener_conexion()
    try:
        with con.cursor() as cur:
            cur.execute(sql, (f"%{texto.strip()}%",))
            rows = cur.fetchall()
            out: List[Dict] = []
            for r in rows:
                out.append({
                    "id_empleado": r["id_empleado"],
                    "nombre": r["nombre"],
                    "direccion": r["direccion"],
                    "correo": r["correo_electronico"],
                    "telefono": r["numero_telefono"],
                    "tipoempleado": r["tipo_empleado"],
                    "fecha_inicio_contrato": _to_datetime(r["fecha_inicio_contrato"]),
                    "salario": float(r["salario"]),
                    "usuario": r["usuario"],
                })
            return out
    finally:
        Conexion().cerrar_conexion(con)

# ----------------- U (Update) -----------------
def editar_empleado_por_id(id_empleado: int, nombre: str, direccion: str,
                           telefono: str, correo: str, fecha_inicio: str | datetime,
                           salario: int | float, usuario: str, tipo_empleado: str) -> int:
    """
    Devuelve cantidad de filas afectadas.
    fecha_inicio: str 'YYYY-MM-DD HH:MM:SS' / 'YYYY-MM-DD' o datetime.
    """
    if isinstance(fecha_inicio, str):
        fi = fecha_inicio.strip()
        try:
            fecha_dt = datetime.strptime(fi, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            fecha_dt = datetime.combine(datetime.strptime(fi, "%Y-%m-%d").date(), datetime.min.time())
    else:
        fecha_dt = fecha_inicio

    tipo_norm = (tipo_empleado or "").strip().lower().capitalize()
    if tipo_norm not in ("Empleado", "Administrativo", "Gerente"):
        raise ValueError("tipo_empleado debe ser: Empleado/Administrativo/Gerente")

    sql = """
    UPDATE empleado
    SET nombre=%s, direccion=%s, numero_telefono=%s, correo_electronico=%s,
        fecha_inicio_contrato=%s, salario=%s, usuario=%s, tipo_empleado=%s
    WHERE id_empleado=%s
    """
    con = Conexion().obtener_conexion()
    try:
        with con.cursor() as cur:
            cur.execute(sql, (
                (nombre or "").strip(),
                (direccion or "").strip(),
                (telefono or "").strip() if telefono is not None else None,
                (correo or "").strip(),
                fecha_dt,
                float(salario),
                (usuario or "").strip(),
                tipo_norm,
                int(id_empleado)
            ))
            affected = cur.rowcount
        con.commit()
        return affected
    except Exception:
        con.rollback()
        raise
    finally:
        Conexion().cerrar_conexion(con)

# ----------------- D (Delete físico) -----------------
def eliminar_empleado_por_id(id_empleado: int) -> int:
    """
    Eliminación FÍSICA. Devuelve filas afectadas (0/1).
    """
    sql = "DELETE FROM empleado WHERE id_empleado=%s"
    con = Conexion().obtener_conexion()
    try:
        with con.cursor() as cur:
            cur.execute(sql, (int(id_empleado),))
            affected = cur.rowcount
        con.commit()
        return affected
    except Exception:
        con.rollback()
        raise
    finally:
        Conexion().cerrar_conexion(con)
