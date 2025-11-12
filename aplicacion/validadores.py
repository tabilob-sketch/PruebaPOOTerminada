# aplicacion/validadores.py
# ==============================================================
# Funciones de validación reutilizables para entradas de usuario.
# ==============================================================

import re

ALLOWED_ROLES = {"admin", "usuario"}

def validar_password(password: str, min_len: int = 8) -> bool:
    if not isinstance(password, str) or not password:
        print("❌ La contraseña no puede estar vacía.")
        return False
    if len(password) < min_len:
        print(f"❌ La contraseña debe tener al menos {min_len} caracteres.")
        return False
    if not re.search(r"[A-Z]", password):
        print("❌ La contraseña debe contener al menos una letra mayúscula.")
        return False
    if not re.search(r"[a-z]", password):
        print("❌ La contraseña debe contener al menos una letra minúscula.")
        return False
    if not re.search(r"[0-9]", password):
        print("❌ La contraseña debe contener al menos un número.")
        return False
    if not re.search(r"[\W_]", password):
        print("❌ La contraseña debe contener al menos un carácter especial (!, *, #, etc.).")
        return False
    return True


def validar_nombre_completo(nombre: str) -> bool:
    if not isinstance(nombre, str) or not nombre.strip():
        print("❌ El nombre no puede estar vacío.")
        return False
    nombre = nombre.strip()
    if len(nombre) < 5:
        print("❌ El nombre es demasiado corto.")
        return False
    if len(nombre) > 60:
        print("❌ El nombre es demasiado largo (máximo 60 caracteres).")
        return False
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
    if not re.match(patron, nombre):
        print("❌ El nombre solo puede contener letras y espacios (sin números ni símbolos).")
        return False
     
    partes = nombre.split()
    if len(partes) < 2:
        print("❌ Debes ingresar al menos nombre y apellido.")
        return False
    return True


def validar_username(username: str) -> bool:
    if not isinstance(username, str) or not username.strip():
        print("❌ El nombre de usuario no puede estar vacío.")
        return False
    username = username.strip()
    if len(username) < 3:
        print("❌ El nombre de usuario es demasiado corto (mínimo 3).")
        return False
    patron = r"^[A-Za-z0-9_]+$"
    if not re.match(patron, username):
        print("❌ El nombre de usuario solo puede contener letras, números o guiones bajos (_).")
        return False
    return True


def validar_login_input(username: str, password: str) -> bool:
    if not isinstance(username, str) or not username.strip():
        print("❌ El nombre de usuario no puede estar vacío.")
        return False
    if not isinstance(password, str) or not password.strip():
        print("❌ La contraseña no puede estar vacía.")
        return False
    return True


ALLOWED_ROLES = {"admin", "usuario"}

def validar_rol(rol: str) -> bool:
    """
    Rol válido solo si:
      - Es string no vacío
      - NO tiene espacios (ni al inicio/fin ni internos)
      - Es exactamente 'admin' o 'usuario' (case-insensitive)
    """
    if not isinstance(rol, str) or not rol:
        print("❌ Rol vacío.")
        return False

    # Rechaza si hay espacios al inicio/fin o internos
    if rol != rol.strip():
        print("❌ El rol no debe contener espacios al inicio o al final.")
        return False
    if " " in rol:
        print("❌ El rol no debe contener espacios.")
        return False

    r = rol.lower()
    if r not in ALLOWED_ROLES:
        print("❌ Rol inválido. Solo 'admin' o 'usuario'.")
        return False
    return True

def normalizar_rol(rol: str) -> str:
    """
    Devuelve 'admin' o 'usuario' si es válido.
    OJO: aquí no hacemos strip; si trae espacios, validar_rol ya habrá fallado.
    """
    r = rol.lower()
    return r if r in ALLOWED_ROLES else ""
        