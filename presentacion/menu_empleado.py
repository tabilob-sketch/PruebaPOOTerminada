# presentacion/menu_empleado.py
from typing import List, Dict, Optional
from persistencia import empleadoDAO      # << importa tu DAO como módulo
import importlib

def _pausar():
    input("\nPresiona ENTER para continuar...")

def _imprimir_detalle(detalle: Optional[Dict]):
    if not detalle:
        print("\nNo se encontró el empleado.")
        return
    print("\n--- Detalle del empleado ---")
    print(f"ID           : {detalle.get('id_empleado')}")
    print(f"Nombre       : {detalle.get('nombre')}")
    print(f"Dirección    : {detalle.get('direccion')}")
    print(f"Correo       : {detalle.get('correo')}")
    print(f"Teléfono     : {detalle.get('telefono')}")
    print(f"TipoEmpleado : {detalle.get('tipoempleado')}")
    if detalle.get("fecha_inicio_contrato"):
        print(f"Fecha inicio : {detalle['fecha_inicio_contrato'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Salario      : {detalle.get('salario')}")
    print(f"Usuario      : {detalle.get('usuario')}")

def _imprimir_listado(rows: List[Dict]):
    if not rows:
        print("\nNo hay empleados registrados.")
        return
    print("\n--- Listado de empleados ---")
    for r in rows:
        fecha_txt = r["fecha_inicio_contrato"].strftime("%Y-%m-%d %H:%M:%S") if r.get("fecha_inicio_contrato") else ""
        print(f"[{r.get('id_empleado')}] {r.get('nombre')} | {r.get('direccion')} | "
              f"{r.get('correo')} | {r.get('telefono')} | {r.get('tipoempleado')} | {fecha_txt} | ${r.get('salario')}")

def _input_creacion():
    print("\n=== Crear empleado ===")
    nombre = input("Nombre: ").strip()
    direccion = input("Dirección: ").strip()
    telefono = input("Teléfono (solo dígitos): ").strip()
    correo = input("Correo: ").strip()
    fecha_inicio = input("Fecha inicio contrato (YYYY-MM-DD HH:MM:SS o YYYY-MM-DD): ").strip()
    salario = input("Salario: ").strip()
    usuario = input("Usuario: ").strip()
    tipo_empleado = input("Tipo de empleado (Empleado/Administrativo/Gerente): ").strip()
    # salario puede venir vacío o con coma
    salario = salario.replace(",", ".") if salario else "0"
    return nombre, direccion, telefono, correo, fecha_inicio, float(salario), usuario, tipo_empleado

def _crear_empleado_runtime(*datos):
    """
    Importa y llama a aplicacion.gestion_empleado.crear_empleado en runtime.
    Si no existe, muestra info útil y no revienta el menú.
    """
    try:
        import aplicacion.gestion_empleado as ge
        importlib.reload(ge)  # por si el archivo fue editado recién
        if not hasattr(ge, "crear_empleado"):
            print(" El módulo no tiene 'crear_empleado'. Pégalo en aplicacion/gestion_empleado.py")
            return
        ge.crear_empleado(*datos)
        print("  Empleado creado.")
    except Exception as e:
        print(f"❌ Error al crear empleado: {e}")

def _input_edicion_con_defaults(det: Dict):
    print("\n=== Editar empleado ===")
    print("Deja en blanco para mantener el valor actual.")
    nombre = input(f"Nombre [{det['nombre']}]: ").strip() or det['nombre']
    direccion = input(f"Dirección [{det['direccion']}]: ").strip() or det['direccion']
    telefono = input(f"Teléfono [{det['telefono']}]: ").strip() or (det['telefono'] or "")
    correo = input(f"Correo [{det['correo']}]: ").strip() or det['correo']

    fecha_def = det['fecha_inicio_contrato'].strftime("%Y-%m-%d %H:%M:%S") if det.get('fecha_inicio_contrato') else ""
    fecha_inicio = input(f"Fecha inicio contrato [{fecha_def}] (YYYY-MM-DD HH:MM:SS o YYYY-MM-DD): ").strip() or fecha_def

    sal_def = str(det['salario'])
    salario_txt = input(f"Salario [{sal_def}]: ").strip()
    salario = float(salario_txt.replace(",", ".")) if salario_txt else float(sal_def)

    usuario = input(f"Usuario [{det['usuario']}]: ").strip() or det['usuario']
    tipo_def = det['tipoempleado']
    tipo_empleado = input(f"Tipo de empleado [{tipo_def}] (Empleado/Administrativo/Gerente): ").strip() or tipo_def

    return nombre, direccion, telefono, correo, fecha_inicio, salario, usuario, tipo_empleado

def menu_empleado():
    while True:
        print("\n==============================")
        print("       Gestión de Empleados")
        print("==============================")
        print("1) Crear empleado")
        print("2) Buscar empleado por ID ")
        print("3) Listar todos los empleados")
        print("4) Buscar empleados por nombre")
        print("5) Editar empleado")
        print("6) Eliminar empleado por id")
        print("0) Volver")
        op = input("Opción: ").strip()

        if op == "1":
            datos = _input_creacion()
            _crear_empleado_runtime(*datos)
            _pausar()

        elif op == "2":
            try:
                _id = int(input("ID del empleado: ").strip())
            except ValueError:
                print("ID inválido.")
                _pausar()
                continue
            detalle = empleadoDAO.buscar_empleado_detalle_por_id(_id)
            _imprimir_detalle(detalle)
            _pausar()

        elif op == "3":
            rows = empleadoDAO.listar_empleados()
            _imprimir_listado(rows)
            _pausar()

        elif op == "4":
            nombre = input("Nombre (o parte): ").strip()
            rows = empleadoDAO.buscar_empleados_por_nombre(nombre)
            _imprimir_listado(rows)
            _pausar()

        elif op == "5":
            # EDITAR
            try:
                _id = int(input("ID a editar: ").strip())
            except ValueError:
                print("ID inválido."); _pausar(); continue

            det = empleadoDAO.buscar_empleado_detalle_por_id(_id)
            if not det:
                print("No existe ese ID."); _pausar(); continue

            datos_edit = _input_edicion_con_defaults(det)
            try:
                affected = empleadoDAO.editar_empleado_por_id(
                    _id,
                    datos_edit[0],  # nombre
                    datos_edit[1],  # direccion
                    datos_edit[2],  # telefono
                    datos_edit[3],  # correo
                    datos_edit[4],  # fecha_inicio
                    datos_edit[5],  # salario
                    datos_edit[6],  # usuario
                    datos_edit[7],  # tipo_empleado
                )
                print(" Editado." if affected else " No se editó ninguna fila.")
            except Exception as e:
                print(f" Error al editar: {e}")
            _pausar()

        elif op == "6":
            # ELIMINAR 
            try:
                _id = int(input("ID a eliminar: ").strip())
            except ValueError:
                print("ID inválido."); _pausar(); continue

            det = empleadoDAO.buscar_empleado_detalle_por_id(_id)
            if not det:
                print("No existe ese ID."); _pausar(); continue

            print(f"Eliminarás a: {det['nombre']} (ID {_id}). ¡Acción irreversible!")
            conf = input("¿Confirmas? (s/n): ").strip().lower()
            if conf in ("s", "si", "y", "yes"):
                try:
                    affected = empleadoDAO.eliminar_empleado_por_id(_id)
                    print(" Eliminado." if affected else "⚠ No se eliminó ninguna fila.")
                except Exception as e:
                    print(f" Error al eliminar: {e}")
            else:
                print("Operación cancelada.")
            _pausar()

        elif op == "0":
            break

        else:
            print("Opción no válida.")
            _pausar()
