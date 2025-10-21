# presentacion/menudepartamento.py
# Menú CRUD para 'Departamento', adaptado a la lógica de métodos estáticos
# y al uso del Enum 'TipoDepartamento'.

from aplicacion.gestiondepartamento import gestiondepartamento
from dominio.departamento import Departamento  # Importamos la clase para acceder al Enum

def _seleccionar_tipo_departamento() -> Departamento.TipoDepartamento:
    """
    Función auxiliar para mostrar los tipos de departamento del Enum
    y permitir al usuario seleccionar uno.
    Retorna el objeto Enum seleccionado (ej. Departamento.TipoDepartamento.ventas)
    """
    print("Seleccione el tipo de departamento:")
    
    # Convertimos el Enum en una lista para poder iterar con un índice
    tipos = list(Departamento.TipoDepartamento)
    
    for i, tipo in enumerate(tipos):
        # Imprimimos: "1. Ventas", "2. Desarrollo", etc.
        print(f"  {i + 1}. {tipo.value}")

    while True:
        try:
            opcion = int(input("Ingrese el número del tipo: "))
            if 1 <= opcion <= len(tipos):
                # Retornamos el objeto Enum correspondiente
                return tipos[opcion - 1] 
            else:
                print("Error: Número fuera de rango.")
        except ValueError:
            print("Error: Ingrese un número válido.")

def _leer_id(mensaje: str) -> int:
    """
    Función auxiliar para leer un ID (entero positivo) de forma segura.
    """
    while True:
        try:
            id_val = int(input(mensaje))
            if id_val > 0:
                return id_val
            else:
                print("Error: El ID debe ser un número positivo.")
        except ValueError:
            print("Error: Ingrese un número válido.")


def menu_departamento():
    """
    Menú de interacción para gestionar Departamentos.
    Utiliza los métodos estáticos de 'gestionDepartamento'.
    """
    while True:
        print("\n------------------------------------------------------------")
        print("          Gestión de Departamentos")
        print("------------------------------------------------------------")
        print("1. Crear Departamento")
        print("2. Editar Departamento")
        print("3. Eliminar Departamento")
        print("4. Buscar Departamento por ID")
        print("5. Salir")
        print("------------------------------------------------------------")
        
        opcion_str = input("Ingrese el Número de la opción: ")

        if not opcion_str.isdigit():
            print("Ingreso una opción no válida, vuelva a intentar.")
            continue
            
        opcion = int(opcion_str)

        if opcion == 1:
            # --- CREAR DEPARTAMENTO ---
            print("\n[1. Creando Nuevo Departamento]")
            nombre = input("Ingrese el nombre del Departamento: ")
            
            # Usamos la función auxiliar para seleccionar el Enum
            tipo_enum = _seleccionar_tipo_departamento()
            
            gestiondepartamento.crear_departamento(nombre, tipo_enum)

        elif opcion == 2:
            # --- EDITAR DEPARTAMENTO ---
            print("\n[2. Editando Departamento]")
            id_depto = _leer_id("Ingrese el ID del departamento a editar: ")
            
            # (Opcional: buscar primero si existe)
            # depto_existente = gestionDepartamento.obtener_departamento_por_id(id_depto)
            # if not depto_existente:
            #     print(f"Error: No se encontró departamento con ID {id_depto}")
            #     continue
            
            print(f"Editando departamento con ID: {id_depto}")
            nombre_nuevo = input("Ingrese el nuevo nombre: ")
            
            # Usamos la función auxiliar para el nuevo tipo
            tipo_nuevo_enum = _seleccionar_tipo_departamento()
            
            gestiondepartamento.editar_departamento(id_depto, nombre_nuevo, tipo_nuevo_enum)

        elif opcion == 3:
            # --- ELIMINAR DEPARTAMENTO ---
            print("\n[3. Eliminando Departamento]")
            id_depto = _leer_id("Ingrese ID del departamento para eliminar: ")
            
            gestiondepartamento.eliminar_departamento(id_depto)

        
        elif opcion == 4:
            # --- BUSCAR POR ID ---
            print("\n[4. Buscar Departamento por ID]")
            id_depto = _leer_id("Ingrese ID del departamento a buscar: ")
            
            depto = gestiondepartamento.obtener_departamento_por_id(id_depto)
            if depto:
                print("Departamento encontrado:")
                print(depto)
            # (El DAO ya imprime un error si no lo encuentra)

        elif opcion == 5:
            # --- SALIR ---
            print("Saliendo del menú de departamentos...")
            break
        
        else:
            print("OPCIÓN NO VÁLIDA. Intente de nuevo.")