# main.py
# ============================================================
# Control de acceso por rol:
# - Admin: acceso completo a todos los menús
# - Usuario: acceso directo al menú de API
# ============================================================

import getpass
from aplicacion.authService import AuthService
from aplicacion.validadores import validar_username
from presentacion.menu_empleado import menu_empleado
from presentacion.menudepartamento import menudepartamento
from presentacion.menuproyecto import menu_proyecto
from presentacion.menu_usuario import menu_usuario
from presentacion.menu_paises import menu_paises   # 👈 tu API

def _pausar():
    input("\nPresiona ENTER para continuar...")

def iniciar_sesion():
    """Login global con validaciones previas y 3 intentos."""
    auth = AuthService()
    intentos = 0
    while intentos < 3:
        print("\n=== INICIO DE SESIÓN ===")

        username = input("Usuario: ").strip()
        if not validar_username(username):
            intentos += 1
            print(f"(Intento {intentos}/3)")
            if intentos < 3:
                _pausar()
            continue

        user_activo = auth.obtener_usuario_activo(username)
        if not user_activo:
            intentos += 1
            print("❌ Usuario no encontrado o inactivo.")
            print(f"(Intento {intentos}/3)")
            if intentos < 3:
                _pausar()
            continue

        password = getpass.getpass("Contraseña: ").strip()
        if not password:
            intentos += 1
            print("❌ La contraseña no puede estar vacía.")
            print(f"(Intento {intentos}/3)")
            if intentos < 3:
                _pausar()
            continue

        try:
            usuario = auth.login(username, password)
            print(f"\n  Bienvenido {usuario.nombre_completo} ({usuario.rol})")
            return usuario
        except ValueError as e:
            intentos += 1
            print(f"❌ {e} (Intento {intentos}/3)")
            if intentos < 3:
                _pausar()
        except Exception as e:
            intentos += 1
            print(f"💥 Error inesperado: {e} (Intento {intentos}/3)")
            if intentos < 3:
                _pausar()

    print("\n🚫 Demasiados intentos fallidos. Cerrando la aplicación...")
    raise SystemExit(1)


def main():
    usuario_actual = iniciar_sesion()

    # === SI ES ADMIN: ACCESO COMPLETO ===
    if usuario_actual.rol.lower() == "admin":
        while True:
            print("\n================================")
            print("          Menú Principal")
            print("================================")
            print("1) Menú Empleados")
            print("2) Menú Departamentos")
            print("3) Menú Proyectos")
            print("4) Menú Usuarios")
            print("5) Países (API)")
            print("0) Salir")

            op = input("Elige una opción: ").strip()

            if op == "1":
                menu_empleado()
            elif op == "2":
                menudepartamento()
            elif op == "3":
                menu_proyecto()
            elif op == "4":
                menu_usuario()
            elif op == "5":
                menu_paises()
            elif op == "0":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("Opción no válida.")
                _pausar()

    # === SI ES USUARIO NORMAL: SOLO API ===
    else:
        print("\n Acceso restringido: solo se permite consultar la API de países.")
        _pausar()
        menu_paises()
        print("\n👋 ¡Hasta luego!")


if __name__ == "__main__":
    main()
