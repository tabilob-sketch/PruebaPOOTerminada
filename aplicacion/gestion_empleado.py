# aplicacion/gestion_empleado.py
# ==============================================================
# CAPA DE APLICACIÓN (o "servicios") PARA EMPLEADOS
# --------------------------------------------------------------
# Esta capa:
#   - Recibe datos desde la presentación (inputs del usuario).
#   - Valida y normaliza esos datos (fechas, enums, strings, etc.).
#   - Crea objetos de dominio (Empleado).
#   - Llama al DAO (acceso a BD) para ejecutar INSERT/UPDATE/DELETE.
#
# Beneficios de esta separación:
#   * Mantiene el menú simple (solo pide datos y muestra resultados).
#   * Centraliza validaciones (menos errores y duplicación).
#   * Facilita pruebas unitarias de lógica sin tocar BD/UI.
# ==============================================================

from datetime import datetime
from dominio.empleado import Empleado
from persistencia import empleadoDAO   # DAO expuesto como módulo (archivo único)

# --------------------------------------------------------------
# PARSERS / VALIDADORES
# --------------------------------------------------------------
# Son funciones pequeñas que convierten el texto del usuario a tipos
# correctos (Enum/fecha). Si algo no cuadra, avisan con un error claro.
# Así evitamos que lleguen datos inválidos a la BD.

def _parse_tipo_empleado(texto: str) -> Empleado.TipoEmpleado:
    """
    Convierte el texto ingresado por el usuario al Enum Empleado.TipoEmpleado.
    Acepta (sin importar mayúsculas/minúsculas):
      - 'empleado'
      - 'administrativo'
      - 'gerente'
    Si el texto no coincide con ninguna opción válida, lanza ValueError con un mensaje explicativo.
    """
    # Normalizamos: quitamos espacios y pasamos a minúsculas para aceptar variantes como "  GeReNte  "
    s = (texto or "").strip().lower()

    # Mapa de palabras válidas -> valor del Enum correspondiente
    mapa = {
        "empleado": Empleado.TipoEmpleado.empleado,
        "administrativo": Empleado.TipoEmpleado.administrativo,
        "gerente": Empleado.TipoEmpleado.gerente,
    }

    # Validación: si el texto no está entre las opciones permitidas, se indica al usuario cómo escribirlo
    if s not in mapa:
        raise ValueError("Tipo de empleado inválido. Usa: Empleado / Administrativo / Gerente")

    # Conversión correcta al Enum
    return mapa[s]

def _parse_fecha(fecha_str: str) -> datetime:
    """
    Convierte una fecha en texto a datetime.
    Formatos admitidos:
      - 'YYYY-MM-DD HH:MM:SS'  (fecha y hora)
      - 'YYYY-MM-DD'           (solo fecha; se asume 00:00:00)
    Si no coincide con ninguno, lanza ValueError indicando el formato correcto.
    """
    fecha_str = (fecha_str or "").strip()

    # Probamos (en orden) con fecha+hora y luego con solo fecha
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(fecha_str, fmt)
            # Si vino solo fecha, fijamos hora 00:00:00 para compatibilidad con DATETIME
            if fmt == "%Y-%m-%d":
                return datetime.combine(dt.date(), datetime.min.time())
            return dt
        except ValueError:
            # Si falla este formato, probamos el siguiente
            pass

    # Si ninguno funcionó, se explica el/los formatos esperados
    raise ValueError("Formato de fecha inválido. Usa 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD'.")

# --------------------------------------------------------------
# C  =  CREATE (INSERT)
# --------------------------------------------------------------

def crear_empleado(
    nombre: str,
    direccion: str,
    telefono: str,
    correo: str,
    fecha_inicio: str,
    salario: int | float,
    usuario: str,
    tipo_empleado_str: str
) -> None:
    """
    Crea un nuevo empleado.
    Flujo:
      1) Validar campos obligatorios.
      2) Convertir tipo_empleado y fecha_inicio a tipos correctos.
      3) Normalizar teléfono (int si son solo dígitos; si no, se guarda como texto).
      4) Construir el objeto de dominio Empleado.
      5) Delegar el INSERT al DAO.
    """
    # 1) Validación mínima: evita registros incompletos en BD
    if not (nombre and direccion and correo and usuario and tipo_empleado_str):
        raise ValueError("Campos obligatorios: nombre, dirección, correo, usuario y tipo_empleado.")

    # 2) Normalización de enum y fecha
    tipo_enum = _parse_tipo_empleado(tipo_empleado_str)
    fecha_dt  = _parse_fecha(fecha_inicio)

    # 3) Teléfono: si son solo dígitos -> int; de lo contrario, guardamos como string (ej. '+56 9 ...')
    tel_texto = (telefono or "").strip()
    tel_valor = int(tel_texto) if tel_texto.isdigit() else tel_texto

    # 4) Construimos el objeto de dominio (lo que tu capa de persistencia espera)
    emp = Empleado(
        id_empleado=None,               # None porque la PK se autogenera (AUTO_INCREMENT)
        nombre=nombre.strip(),
        direccion=direccion.strip(),
        numero_telefono=tel_valor,
        correo_electronico=correo.strip(),
        fecha_inicio_contrato=fecha_dt, # datetime ya validado
        salario=float(salario),         # forzamos a float por consistencia
        usuario=usuario.strip(),
        tipo_empleado=tipo_enum
    )

    # 5) Enviar al DAO para que haga el INSERT real en la BD
    empleadoDAO.insert_empleado(emp)

# --------------------------------------------------------------
# U  =  UPDATE
# --------------------------------------------------------------

def editar_empleado(
    id_empleado: int,
    nombre: str,
    direccion: str,
    telefono: str,
    correo: str,
    fecha_inicio: str,
    salario: int | float,
    usuario: str,
    tipo_empleado_str: str
) -> int:
    """
    Edita un empleado existente por su ID.
    Retorna: cantidad de filas afectadas (0 si no existía / 1 si se actualizó).
    Pasos:
      1) Convertir tipo_empleado y fecha_inicio a tipos correctos.
      2) Normalizar teléfono.
      3) Limpiar espacios en strings.
      4) Llamar al DAO para hacer el UPDATE.
    """
    # 1) Validaciones/conversiones clave
    tipo_enum = _parse_tipo_empleado(tipo_empleado_str)
    fecha_dt  = _parse_fecha(fecha_inicio)

    # 2) Teléfono: mismo criterio que en "crear"
    tel_txt  = (telefono or "").strip()
    tel_norm = int(tel_txt) if tel_txt.isdigit() else tel_txt

    # 3) Llamada al DAO:
    #    - fecha_inicio como string con hora para consistencia.
    #    - tipo_empleado como texto (value del Enum), útil si la columna es ENUM en MySQL.
    filas = empleadoDAO.editar_empleado_por_id(
        id_empleado=int(id_empleado),
        nombre=(nombre or "").strip(),
        direccion=(direccion or "").strip(),
        telefono=str(tel_norm) if tel_norm is not None else None,
        correo=(correo or "").strip(),
        fecha_inicio=fecha_dt.strftime("%Y-%m-%d %H:%M:%S"),
        salario=float(salario),
        usuario=(usuario or "").strip(),
        tipo_empleado=tipo_enum.value
    )
    return filas

# --------------------------------------------------------------
# D  =  DELETE (ELIMINACIÓN DE LA BD)
# --------------------------------------------------------------

def eliminar_empleado(id_empleado: int) -> int:
    """
    Elimina físicamente (DELETE) un empleado por su ID.
    Retorna: filas afectadas (0 si no existía / 1 si se borró).
    Nota: "eliminación física" significa que el registro desaparece de la BD;
          si prefieres eliminación lógica, habría que usar un campo 'activo=0'.
    """
    return empleadoDAO.eliminar_empleado_por_id(int(id_empleado))
