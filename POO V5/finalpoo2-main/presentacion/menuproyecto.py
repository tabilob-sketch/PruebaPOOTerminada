from aplicacion.gestionproyecto import gestionProyecto
from datetime import datetime #Importamos datetime para gestionar la fecha dentro del proyecto

#Aqui vamos hacer el menu de interaccion de usuario con Proyecto haciendo que desde la capa de presentacion interactuemos con las diferentes capas dentro del proyecto

def menu_proyecto():
    while True:
        print("------------------------------------------------------------")
        print("1. Crear Proyecto")
        print("2. Editar Proyecto")
        print("3. Eliminar Proyecto")
        print("4. Salir")
        print("------------------------------------------------------------")
        try:
            opcion = int(input("Ingrese el Numero de la opcion: ")) 
        except ValueError:
            print("Ingreso una opcion no valida vuelva a intentar")
        if opcion == 1:
            nombre = input("Ingrese el nombre del Proyecto: ")
            descripcion = input("Ingrese la descripcion del Proyecto: ")
            fecha = input("Ingrese la fecha del inicio del proyecto (AÑO-MES-DIA): ")

            #Conversion de fecha -> str a fecha -> datetime
            fecha_formateada = datetime.strptime(fecha, "%y-%m-%d")

            gestionProyecto.crear_proyecto(nombre, descripcion, fecha)
    
        elif opcion == 2:
            id_proyecto = int(input("Ingrese el ID del proyecto: "))
            nombre_nuevo = input("Ingrese el nuevo nombre del Proyecto: ")
            descripcion_nueva = input("Ingrese la nueva descripcion del Proyecto: ")
            fecha_nueva = input("Ingrese la nueva fecha del Proyecto (AÑO-MES-DIA): ")

            #Conversion de fecha -> str a fecha -> datetime
            fecha_nueva_formateada = datetime.strptime(fecha_nueva, "%y-%m-%d")
            gestionProyecto.editar_proyecto(id_proyecto, nombre_nuevo, descripcion_nueva,fecha_nueva_formateada)

        elif opcion == 3:
            id_proyecto = int(input("Ingrese ID del proyecto para eliminar: "))
            gestionProyecto.eliminar_proyecto(id_proyecto)
    
        else:
            print("OPCION NO VALIDA EN EL MENU")
        return opcion 