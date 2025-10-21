# presentacion/menutipodepartamento.py
# Menú CRUD para el catálogo 'tipo_departamento'.

from aplicacion.gestiontipodepartamento import GestionTipoDepartamento

def _leer_int(msg: str) -> int:
    # Lee un entero por consola (reintenta si hay error)
    while True:
        v = input(msg).strip()
        if v.isdigit(): return int(v)
        print("Ingrese un numero valido.")

def menu_tipo_departamento():
    svc = GestionTipoDepartamento()
    while True:
        print("\n=== Tipo de Departamento ===")
        print("1) Crear  2) Listar  3) Editar  4) Eliminar  0) Volver")
        op = input("> ").strip()

        if op == "1":  # Crear
            try:
                new_id = svc.crear(input("Nombre del tipo: "))
                print(f"Creado con id {new_id}")
            except Exception as e:
                print("Error:", e)

        elif op == "2":  # Listar
            tipos = svc.listar()
            if not tipos: print("(sin tipos)")
            for t in tipos: print(f"[{t.id_tipo_departamento}] {t.nombre}")

        elif op == "3":  # Editar
            try:
                ok = svc.editar(_leer_int("ID a editar: "), input("Nuevo nombre: "))
                print("Actualizado" if ok else "No se encontro")
            except Exception as e:
                print("Error:", e)

        elif op == "4":  # Eliminar
            try:
                ok = svc.eliminar(_leer_int("ID a eliminar: "))
                print("Eliminado" if ok else "No se encontro")
            except Exception as e:
                print("Error:", e)

        elif op == "0":
            break
        else:
            print("Opcion invalida")
