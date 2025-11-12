# aplicacion/authService.py
# ==============================================================
# Servicio de autenticación.
# - Login con verificación de hash (bcrypt)
# - Permite validar si un usuario existe y está activo
# ==============================================================

from persistencia.usuarioDAO import UsuarioDAO
from aplicacion.seguridad import verificar_password

class AuthService:
    def __init__(self):
        self.dao = UsuarioDAO()

    def obtener_usuario_activo(self, username: str):
        """
        Retorna el objeto Usuario si existe y está activo.
        Devuelve None si el usuario no existe o está inactivo.
        Esto se usa para validar antes de pedir la contraseña.
        """
        if not isinstance(username, str) or not username.strip():
            return None

        user = self.dao.obtener_por_username(username.strip())
        if user and getattr(user, "activo", False):
            return user
        return None

    def login(self, username: str, password: str):
        """
        Autentica al usuario validando su contraseña encriptada.
        """
        if not username.strip():
            raise ValueError("El usuario no puede estar vacío.")
        if not password.strip():
            raise ValueError("La contraseña no puede estar vacía.")

        user = self.dao.obtener_por_username(username.strip())

        if user is None or not getattr(user, "activo", False):
            raise ValueError("Usuario no encontrado o inactivo.")

        if not verificar_password(password, user.password_hash):
            raise ValueError("Contraseña incorrecta.")

        return user
