# presentacion/menuprincipal.py
# Menú raíz: navega a Tipos y Departamentos

from presentacion.menutipodepartamento import menu_tipo_departamento
from presentacion.menudepartamento import menu_departamento

def menu_principal():
    while True:
        print("------------------------------------------------------------")
        print("1) Tipos de Departamento")
        print("2) Departamentos")
        print("0) Salir")
        op = input("> ").strip()
        print("------------------------------------------------------------")

        if op == "1":
            menu_tipo_departamento()   # abre el CRUD de TIPOS
        elif op == "2":
            menu_departamento()        # abre el CRUD de DEPARTAMENTOS
        elif op == "0":
            break
        else:
            print("Opcion invalida")
