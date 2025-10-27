# main.py
# Menú principal: Empleados / Departamentos / Proyectos

from presentacion.menu_empleado import menu_empleado
from presentacion.menudepartamento import menudepartamento
from presentacion.menuproyecto import menu_proyecto

def _pausar():
    input("\nPresiona ENTER para continuar...")

def main():
    while True:
        print("\n================================")
        print("          Menú Principal")
        print("================================")
        print("1) Menú Empleados")
        print("2) Menú Departamentos")
        print("3) Menú Proyectos")
        print("0) Salir")
        op = input("Elige una opción: ").strip()

        if op == "1":
            menu_empleado()
        elif op == "2":
            menudepartamento()
        elif op == "3":
            menu_proyecto()
        elif op == "0":
            print("¡Hasta luego! ")
            break
        else:
            print("Opción no válida.")
            _pausar()

if __name__ == "__main__":
    main()
