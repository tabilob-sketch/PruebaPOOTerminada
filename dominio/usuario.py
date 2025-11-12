# dominio/usuario.py

class Usuario:
    def __init__(self, id=None, username="", password_hash="", nombre_completo="", rol="usuario", activo=True):
        self.id = id
        self.username = username
        self.password_hash = password_hash  # siempre hash, nunca texto plano
        self.nombre_completo = nombre_completo
        self.rol = rol  # 'admin' o 'usuario'
        self.activo = bool(activo)

    def __repr__(self):
        return f"Usuario(id={self.id}, username='{self.username}', rol='{self.rol}', activo={self.activo})"

    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"[{self.id}] {self.username} - {self.nombre_completo} ({self.rol}) - {estado}"
