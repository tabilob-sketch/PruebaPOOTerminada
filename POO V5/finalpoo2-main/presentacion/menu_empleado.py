# presentacion/menu_empleado.py
from aplicacion.gestion_empleado import gestionempleado
from datetime import datetime

def menu_empleado():
    print("\n--- MENÚ EMPLEADOS ---")
    print("1. Crear empleado")
    print("2. Buscar empleado")
    print("3. Editar empleado")
    print("4. Eliminar empleado")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input("Nombre: ")
        direccion = input("Dirección: ")
        telefono = int(input("Teléfono: "))
        correo = input("Correo: ")
        fecha_inicio = datetime.strptime(input("Fecha de inicio (YYYY-MM-DD): "), "%Y-%m-%d")
        salario = int(input("Salario: "))
        usuario = input("Usuario: ")
        tipo_empleado = input("Tipo de empleado (Empleado/Administrativo/Gerente): ")
        gestionempleado.crear_empleado(nombre, direccion, telefono, correo, fecha_inicio, salario, usuario, tipo_empleado)

    elif opcion == "2":
        id_empleado = int(input("ID del empleado: "))
        gestionempleado.buscar_empleado(id_empleado)

    elif opcion == "3":
        id_empleado = int(input("ID del empleado a editar: "))
        nombre = input("Nuevo nombre: ")
        direccion = input("Nueva dirección: ")
        telefono = int(input("Nuevo teléfono: "))
        correo = input("Nuevo correo: ")
        fecha_inicio = datetime.strptime(input("Nueva fecha de inicio (YYYY-MM-DD): "), "%Y-%m-%d")
        salario = int(input("Nuevo salario: "))
        usuario = input("Nuevo usuario: ")
        tipo_empleado = input("Nuevo tipo de empleado (Empleado/Administrativo/Gerente): ")
        gestionempleado.editar_empleado(id_empleado, nombre, direccion, telefono, correo, fecha_inicio, salario, usuario, tipo_empleado)

    elif opcion == "4":
        id_empleado = int(input("ID del empleado a eliminar: "))
        gestionempleado.eliminar_empleado(id_empleado)