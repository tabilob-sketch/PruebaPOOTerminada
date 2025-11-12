# aplicacion/seguridad.py
# Encriptación y verificación de contraseñas con bcrypt

import bcrypt

def encriptar_password(password_plano: str) -> str:
    """
    Genera un hash seguro (bcrypt) a partir de una contraseña en texto plano.
    Devuelve el hash en string (utf-8) para guardarlo en la BD.
    """
    if not isinstance(password_plano, str) or not password_plano:
        raise ValueError("La contraseña no puede estar vacía y debe ser str.")
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_plano.encode("utf-8"), salt)
    return password_hash.decode("utf-8")

def verificar_password(password_plano: str, password_hash: str) -> bool:
    """
    Compara una contraseña en texto plano contra su hash almacenado.
    Retorna True si coincide, False en caso contrario.
    """
    if not password_hash:
        return False
    try:
        return bcrypt.checkpw(password_plano.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False
