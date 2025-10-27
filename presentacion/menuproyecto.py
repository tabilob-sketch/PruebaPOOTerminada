# presentacion/menuproyecto.py
from aplicacion.gestionproyecto import gestionProyecto
from datetime import datetime

def _pausar():
    input("\nPresiona ENTER para continuar...")

def _imprimir_listado(rows):
    if not rows:
        print("\nNo hay proyectos para mostrar.")
        return
    print("\n--- Listado de proyectos ---")
    for r in rows:
        fi = r.get("fecha_inicio")
        fi_txt = fi.strftime("%Y-%m-%d") if hasattr(fi, "strftime") else (fi or "")
        print(f"[{r.get('id_proyecto')}] {r.get('nombre')} | {r.get('descripcion') or ''} | Inicio: {fi_txt}")

def menu_proyecto():
    while True:
        print("------------------------------------------------------------")
        print("1. Crear Proyecto")
        print("2. Editar Proyecto")
        print("3. Eliminar Proyecto")
        print("4. Listar TODOS los proyectos")          # ✅ NUEVO
        print("5. Buscar proyectos por NOMBRE")         # ✅ NUEVO
        print("0. Volver")
        print("------------------------------------------------------------")
        try:
            opcion = int(input("Ingrese el Número de la opción: ").strip())
        except ValueError:
            print("Ingresaste una opción no válida. Intenta de nuevo.")
            _pausar()
            continue

        if opcion == 1:
            nombre = input("Ingrese el nombre del Proyecto: ").strip()
            descripcion = input("Ingrese la descripción del Proyecto: ").strip()
            fecha = input("Ingrese la fecha de inicio (AAAA-MM-DD): ").strip()

            # Conversión de fecha -> datetime (corrige %Y en vez de %y)
            try:
                fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                print("Formato de fecha inválido. Usa AAAA-MM-DD.")
                _pausar()
                continue

            # Tu capa de aplicación puede aceptar str o datetime; si espera str, pasa fecha (str)
            gestionProyecto.crear_proyecto(nombre, descripcion, fecha_formateada)
            _pausar()

        elif opcion == 2:
            try:
                id_proyecto = int(input("Ingrese el ID del proyecto: ").strip())
            except ValueError:
                print("ID inválido."); _pausar(); continue

            nombre_nuevo = input("Ingrese el nuevo nombre: ").strip()
            descripcion_nueva = input("Ingrese la nueva descripción: ").strip()
            fecha_nueva = input("Nueva fecha (AAAA-MM-DD): ").strip()
            try:
                fecha_nueva_formateada = datetime.strptime(fecha_nueva, "%Y-%m-%d")
            except ValueError:
                print("Formato de fecha inválido. Usa AAAA-MM-DD.")
                _pausar()
                continue

            gestionProyecto.editar_proyecto(id_proyecto, nombre_nuevo, descripcion_nueva, fecha_nueva_formateada)
            _pausar()

        elif opcion == 3:
            try:
                id_proyecto = int(input("Ingrese ID del proyecto para eliminar: ").strip())
            except ValueError:
                print("ID inválido."); _pausar(); continue
            gestionProyecto.eliminar_proyecto(id_proyecto)
            _pausar()

        elif opcion == 4:  # ✅ LISTAR TODOS
            rows = gestionProyecto.listar_todos()
            _imprimir_listado(rows)
            _pausar()

        elif opcion == 5:  # ✅ BUSCAR POR NOMBRE
            nombre = input("Nombre (o parte): ").strip()
            rows = gestionProyecto.buscar_por_nombre(nombre)
            _imprimir_listado(rows)
            _pausar()

        elif opcion == 0:
            break

        else:
            print("Opción no válida.")
            _pausar()
