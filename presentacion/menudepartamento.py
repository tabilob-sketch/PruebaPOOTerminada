# presentacion/menudepartamento.py
print(">> menudepartamento (con opciones 5 y 6) cargado desde:", __file__)

from aplicacion.gestiondepartamento import gestiondepartamento
from dominio.departamento import Departamento  # para el Enum

def _pausar():
    input("\nPresiona ENTER para continuar...")

def _imprimir_listado(rows):
    if not rows:
        print("\nNo hay departamentos registrados.")
        return
    print("\n--- Listado de departamentos ---")
    for r in rows:
        print(f"[{r.get('id_departamento')}] {r.get('nombre')} | {r.get('tipo_departamento')}")

def _seleccionar_tipo_departamento() -> Departamento.TipoDepartamento:
    print("Seleccione el tipo de departamento:")
    tipos = list(Departamento.TipoDepartamento)
    for i, tipo in enumerate(tipos, start=1):
        print(f"  {i}. {tipo.value}")
    while True:
        try:
            opcion = int(input("Ingrese el número del tipo: "))
            if 1 <= opcion <= len(tipos):
                return tipos[opcion - 1]
            else:
                print("Error: Número fuera de rango.")
        except ValueError:
            print("Error: Ingrese un número válido.")

def _leer_id(mensaje: str) -> int:
    while True:
        try:
            id_val = int(input(mensaje))
            if id_val > 0:
                return id_val
            else:
                print("Error: El ID debe ser positivo.")
        except ValueError:
            print("Error: Ingrese un número válido.")

def menudepartamento():
    while True:
        print("\n------------------------------------------------------------")
        print("          Gestión de Departamentos")
        print("------------------------------------------------------------")
        print("1. Crear Departamento")
        print("2. Editar Departamento")
        print("3. Eliminar Departamento")
        print("4. Buscar Departamento por ID")
        print("5. Listar todos los Departamentos")   # ← NUEVA
        print("6. Buscar Departamentos por nombre") # ← NUEVA
        print("0. Volver")
        print("------------------------------------------------------------")

        opcion = input("Ingrese el Número de la opción: ").strip()

        if opcion == "1":
            print("\n[1. Creando Nuevo Departamento]")
            nombre = input("Ingrese el nombre del Departamento: ").strip()
            tipo_enum = _seleccionar_tipo_departamento()
            gestiondepartamento.crear_departamento(nombre, tipo_enum)
            _pausar()

        elif opcion == "2":
            print("\n[2. Editando Departamento]")
            id_depto = _leer_id("Ingrese el ID del departamento a editar: ")
            nombre_nuevo = input("Ingrese el nuevo nombre: ").strip()
            tipo_nuevo_enum = _seleccionar_tipo_departamento()
            gestiondepartamento.editar_departamento(id_depto, nombre_nuevo, tipo_nuevo_enum)
            _pausar()

        elif opcion == "3":
            print("\n[3. Eliminando Departamento]")
            id_depto = _leer_id("Ingrese ID del departamento para eliminar: ")
            gestiondepartamento.eliminar_departamento(id_depto)
            _pausar()

        elif opcion == "4":
            print("\n[4. Buscar Departamento por ID]")
            id_depto = _leer_id("Ingrese ID del departamento a buscar: ")
            depto = gestiondepartamento.obtener_departamento_por_id(id_depto)
            if depto:
                print("Departamento encontrado:\n", depto)
            else:
                print("No se encontró el departamento.")
            _pausar()

        elif opcion == "5":  # ← LISTAR TODOS
            rows = gestiondepartamento.listar_departamentos()
            _imprimir_listado(rows)
            _pausar()

        elif opcion == "6":  # ← BUSCAR POR NOMBRE
            nombre = input("Ingrese nombre (o parte): ").strip()
            rows = gestiondepartamento.buscar_departamentos_por_nombre(nombre)
            _imprimir_listado(rows)
            _pausar()

        elif opcion == "0":
            print("Volviendo al menú principal...")
            break

        else:
            print("OPCIÓN NO VÁLIDA. Intente de nuevo.")
            _pausar()
