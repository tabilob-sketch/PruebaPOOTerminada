# aplicacion/usuarioService.py
# ==============================================================
# Servicio de gestión de usuarios (CRUD seguro)
# Usa hashing de contraseñas con bcrypt
# ==============================================================

from persistencia.usuarioDAO import UsuarioDAO
from aplicacion.seguridad import encriptar_password
from aplicacion.validadores import validar_rol, normalizar_rol
from aplicacion.errores import DuplicadoError, NoEncontradoError
from dominio.usuario import Usuario


class UsuarioService:
    """
    Capa de aplicación para el manejo de usuarios.
    Encapsula la lógica de negocio (hash de contraseñas, validaciones, etc.).
    """

    def __init__(self):
        self.dao = UsuarioDAO()

    # Utilidad opcional (por si quieres pre-chequear en UI)
    def buscar_por_username(self, username: str):
        return self.dao.obtener_por_username(username)

    def crear_usuario(self, username: str, password: str, nombre: str, rol: str = "usuario") -> int:
        # Validación/normalización de rol
        if not validar_rol(rol):
            raise ValueError("Rol inválido. Debe ser 'admin' o 'usuario'.")
        rol = normalizar_rol(rol)

        # Pre-check duplicado para feedback rápido
        if self.dao.obtener_por_username(username):
            raise DuplicadoError("username", username)

        hash_pass = encriptar_password(password)
        usuario = Usuario(
            username=username,
            password_hash=hash_pass,
            nombre_completo=nombre,
            rol=rol,
            activo=True,
        )
        # Si por carrera aún choca, el DAO lanzará DuplicadoError
        return self.dao.crear(usuario)

    def modificar_usuario(
        self,
        id_usuario: int,
        username: str = "",
        password: str = "",
        nombre: str = "",
        rol: str = "",
        activo: bool = True,
    ) -> bool:
        usuario_existente = self.dao.buscar_por_id(id_usuario)
        if not usuario_existente:
            raise NoEncontradoError("Usuario")

        # Si cambió username → validar duplicado
        if username and username != usuario_existente.username:
            if self.dao.obtener_por_username(username):
                raise DuplicadoError("username", username)
            usuario_existente.username = username

        if password:
            usuario_existente.password_hash = encriptar_password(password)
        if nombre:
            usuario_existente.nombre_completo = nombre
        if rol:
            if not validar_rol(rol):
                raise ValueError("Rol inválido. Debe ser 'admin' o 'usuario'.")
            usuario_existente.rol = normalizar_rol(rol)

        usuario_existente.activo = bool(activo)

        return self.dao.modificar(usuario_existente)

    def eliminar_usuario(self, id_usuario: int) -> bool:
        return self.dao.eliminar(id_usuario)

    def buscar_por_id(self, id_usuario: int):
        return self.dao.buscar_por_id(id_usuario)

    def listar_todos(self):
        return self.dao.listar_todos()
