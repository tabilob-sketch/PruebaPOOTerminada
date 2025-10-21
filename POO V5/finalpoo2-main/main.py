# main.py
# Punto de entrada: arranca el menú principal.

from presentacion.menudepartamento import menu_departamento
from presentacion.menuproyecto import menu_proyecto
from presentacion.menu_empleado import menu_empleado

if __name__ == "__main__":
    menu_empleado()
    menu_departamento()
    menu_proyecto()
