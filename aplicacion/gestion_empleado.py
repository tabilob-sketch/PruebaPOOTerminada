# aplicacion/gestion_empleado.py
# aplicacion/gestion_empleado.py
from datetime import datetime
from dominio.empleado import Empleado
from persistencia import empleadoDAO   # ✅ Import correcto del DAO

# ------------------ Parsers / Validaciones ------------------

def _parse_tipo_empleado(texto: str) -> Empleado.TipoEmpleado:
    s = (texto or "").strip().lower()
    mapa = {
        "empleado": Empleado.TipoEmpleado.empleado,
        "administrativo": Empleado.TipoEmpleado.administrativo,
        "gerente": Empleado.TipoEmpleado.gerente,
    }
    if s not in mapa:
        raise ValueError("Tipo de empleado inválido. Usa: Empleado / Administrativo / Gerente")
    return mapa[s]

def _parse_fecha(fecha_str: str) -> datetime:
    fecha_str = (fecha_str or "").strip()
    # Permitir "YYYY-MM-DD HH:MM:SS" o "YYYY-MM-DD"
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(fecha_str, fmt)
            # si vino solo fecha, la dejamos a las 00:00:00
            if fmt == "%Y-%m-%d":
                return datetime.combine(dt.date(), datetime.min.time())
            return dt
        except ValueError:
            pass
    raise ValueError("Formato de fecha inválido. Usa 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD'.")

# ------------------ C (Create) ------------------

def crear_empleado(nombre: str, direccion: str, telefono: str, correo: str,
                   fecha_inicio: str, salario: int | float, usuario: str, tipo_empleado_str: str) -> None:
    """
    LLAMADA DESDE TU MENÚ:
    _crear_empleado_runtime(*datos) -> crear_empleado(nombre, direccion, telefono, correo, fecha_inicio, salario, usuario, tipo)
    """
    if not (nombre and direccion and correo and usuario and tipo_empleado_str):
        raise ValueError("Campos obligatorios: nombre, dirección, correo, usuario y tipo_empleado.")

    tipo_enum = _parse_tipo_empleado(tipo_empleado_str)
    fecha_dt = _parse_fecha(fecha_inicio)

    emp = Empleado(
        id_empleado=None,
        nombre=nombre.strip(),
        direccion=direccion.strip(),
        numero_telefono=int(telefono) if (telefono or "").strip().isdigit() else telefono.strip(),  # acepta dígitos o texto
        correo_electronico=correo.strip(),
        fecha_inicio_contrato=fecha_dt,
        salario=float(salario),
        usuario=usuario.strip(),
        tipo_empleado=tipo_enum
    )

    # INSERT: delegamos al DAO de módulo (crea registro)
    # Si tu DAO aún no tiene esta función, créala como 'insert_empleado(emp)'
    empleadoDAO.insert_empleado(emp)

# ------------------ U (Update) ------------------

def editar_empleado(id_empleado: int, nombre: str, direccion: str, telefono: str, correo: str,
                    fecha_inicio: str, salario: int | float, usuario: str, tipo_empleado_str: str) -> int:
    """
    Edita un empleado por ID. Devuelve filas afectadas (0/1).
    """
    tipo_enum = _parse_tipo_empleado(tipo_empleado_str)
    fecha_dt = _parse_fecha(fecha_inicio)

    # Permitimos dejar igual algún campo si viene vacío (útil si haces un flujo interactivo)
    # Aquí asumo que te pasan todos los campos ya resueltos. Si quieres 'dejar en blanco = mantener',
    # primero lee el registro y completa defaults antes de llamar a esta función.
    telefono_norm = (telefono or "").strip()
    telefono_norm = int(telefono_norm) if telefono_norm.isdigit() else telefono_norm

    return empleadoDAO.editar_empleado_por_id(
        id_empleado=int(id_empleado),
        nombre=(nombre or "").strip(),
        direccion=(direccion or "").strip(),
        telefono=str(telefono_norm) if telefono_norm is not None else None,
        correo=(correo or "").strip(),
        fecha_inicio=fecha_dt.strftime("%Y-%m-%d %H:%M:%S"),
        salario=float(salario),
        usuario=(usuario or "").strip(),
        tipo_empleado=tipo_enum.value  # pasamos el texto del Enum
    )

# ------------------ D (Delete) ------------------

def eliminar_empleado(id_empleado: int) -> int:
    """
    Eliminación FÍSICA por ID. Devuelve filas afectadas (0/1).
    """
    return empleadoDAO.eliminar_empleado_por_id(int(id_empleado))


