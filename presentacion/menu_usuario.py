# presentacion/menu_usuario.py
# =====================================================
# CRUD de usuarios (acceso controlado desde main.py)
# Usa validadores centralizados e interacción robusta.
# =====================================================

import getpass
from aplicacion.usuarioService import UsuarioService
from aplicacion.validadores import (
    validar_password,
    validar_nombre_completo,
    validar_username,
    validar_rol,
    normalizar_rol,
)
from aplicacion.errores import DuplicadoError

def _pausar():
    input("\nPresiona ENTER para continuar...")

def _txt_activo(flag: bool) -> str:
    return "Sí" if bool(flag) else "No"


def menu_usuario():
    service = UsuarioService()

    while True:
        print("\n==============================")
        print("       Gestión de Usuarios")
        print("==============================")
        print("1) Crear usuario")
        print("2) Modificar usuario")
        print("3) Eliminar usuario")
        print("4) Buscar usuario por ID")
        print("5) Listar todos los usuarios")
        print("0) Volver")
        op = input("Opción: ").strip()

        try:
            # ======================================================
            # CREAR USUARIO (duplicado detectado temprano)
            # ======================================================
            if op == "1":
                # Username: validación de formato y duplicado inmediato
                while True:
                    username = input("Username: ").strip()
                    if not validar_username(username):
                        print("  Username inválido. Solo letras, números o '_'.\n")
                        continue
                    if service.buscar_por_username(username):
                        print(f"  Username ya existente: '{username}'. Ingresa otro.\n")
                        continue
                    break

                # Password (oculta al escribir)
                while True:
                    password = getpass.getpass("Password: ").strip()
                    if validar_password(password):
                        break
                    print("  Contraseña inválida. Debe tener al menos 8 caracteres, una mayúscula, un número y un símbolo.\n")

                # Nombre completo
                while True:
                    nombre = input("Nombre completo: ").strip()
                    if validar_nombre_completo(nombre):
                        break
                    print("  Nombre inválido. Solo letras y espacios.\n")

                # Rol (sin espacios, exacto)
                while True:
                    rol_input = input("Rol (admin/usuario): ").strip()
                    if validar_rol(rol_input):
                        rol = normalizar_rol(rol_input)
                        break
                    print("  Rol inválido. Solo 'admin' o 'usuario' (sin espacios).\n")

                # Intento de creación
                try:
                    nuevo_id = service.crear_usuario(username, password, nombre, rol)
                    print(f"  Usuario creado con ID {nuevo_id}")
                    _pausar()
                except DuplicadoError as de:
                    print(f"  {de.campo} ya existente: '{de.valor}'. Ingresa otro.\n")
                    _pausar()

            # ======================================================
            # MODIFICAR USUARIO
            # ======================================================
            elif op == "2":
                try:
                    id_usuario = int(input("ID del usuario a modificar: ").strip())
                except ValueError:
                    print("  ID inválido.")
                    _pausar()
                    continue

                u = service.buscar_por_id(id_usuario)
                if not u:
                    print("  Usuario no encontrado.")
                    _pausar()
                    continue

                print("\n--- Valores actuales ---")
                print(f"ID: {u.id}")
                print(f"Username      : {u.username}")
                print(f"Nombre completo: {u.nombre_completo}")
                print(f"Rol           : {u.rol}")
                print(f"Activo        : {_txt_activo(u.activo)}")
                print("(Deja en blanco para mantener el valor actual)\n")

                # USERNAME
                while True:
                    username = input(f"Nuevo username [{u.username}]: ").strip()
                    if not username:
                        username = ""
                        break
                    if not validar_username(username):
                        print("  Username inválido. Solo letras, números y guión bajo.\n")
                        continue
                    if username != u.username and service.buscar_por_username(username):
                        print(f"  Username ya existente: '{username}'. Ingresa otro.\n")
                        continue
                    break

                # PASSWORD (oculta al escribir)
                while True:
                    password = getpass.getpass("Nueva contraseña (ENTER para mantener): ").strip()
                    if not password:
                        break
                    if validar_password(password):
                        break
                    print("  Contraseña inválida. Debe tener al menos 8 caracteres, una mayúscula, un número y un símbolo.\n")

                # NOMBRE COMPLETO
                while True:
                    nombre = input(f"Nuevo nombre completo [{u.nombre_completo}]: ").strip()
                    if not nombre:
                        nombre = ""
                        break
                    if validar_nombre_completo(nombre):
                        break
                    print("  Nombre inválido. Solo letras y espacios.\n")

                # ROL
                while True:
                    rol_in = input(f"Nuevo rol (admin/usuario) [{u.rol}]: ").strip()
                    if not rol_in:
                        rol = ""
                        break
                    if validar_rol(rol_in):
                        rol = normalizar_rol(rol_in)
                        break
                    print("  Rol inválido. Solo 'admin' o 'usuario' (sin espacios).\n")

                # ACTIVO
                while True:
                    activo_str = input(f"Activo? (s/n) [{'s' if u.activo else 'n'}]: ").strip().lower()
                    if activo_str == "":
                        activo = u.activo
                        break
                    if activo_str in ("s", "n"):
                        activo = (activo_str == "s")
                        break
                    print("  Valor inválido. Solo 's' o 'n'.\n")

                service.modificar_usuario(id_usuario, username, password, nombre, rol, activo)
                print("  Usuario actualizado correctamente.")
                _pausar()

            elif op == "3":
                try:
                    id_usuario = int(input("ID del usuario a eliminar: ").strip())
                except ValueError:
                    print("  ID inválido.")
                    _pausar()
                    continue
                service.eliminar_usuario(id_usuario)
                print("  Usuario eliminado correctamente.")
                _pausar()

            elif op == "4":
                try:
                    id_usuario = int(input("ID del usuario: ").strip())
                except ValueError:
                    print("  ID inválido.")
                    _pausar()
                    continue
                u = service.buscar_por_id(id_usuario)
                print(u if u else "  Usuario no encontrado.")
                _pausar()

            elif op == "5":
                usuarios = service.listar_todos()
                if not usuarios:
                    print("No hay usuarios registrados.")
                else:
                    print("\n--- LISTA DE USUARIOS ---")
                    for u in usuarios:
                        print(u)
                _pausar()

            elif op == "0":
                break

            else:
                print("Opción no válida.")
                _pausar()

        except ValueError as e:
            print(f"  Error: {e}")
            _pausar()
        except Exception as e:
            print(f"  Error inesperado: {e}")
            _pausar()
