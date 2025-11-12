# presentacion/menu_paises.py
# ==============================================================
# Menú para consultar API pública (REST Countries)
# ==============================================================

from api.api_paises import ApiPaisesService

def _pausar():
    input("\nPresiona ENTER para continuar...")

def _imprimir_detalle(p: dict):
    print("\n--- Detalle del País ---")
    print(f"Nombre común     : {p['nombre_comun']}")
    print(f"Nombre oficial   : {p['nombre_oficial']}")
    print(f"Códigos          : {p['codigo_cca2']} / {p['codigo_cca3']}")
    print(f"Región/Subregión : {p['region']} / {p['subregion']}")
    print(f"Capital          : {p['capital']}")
    print(f"Población        : {p['poblacion']:,}")
    print(f"Área (km²)       : {p['area_km2']:,}")
    print(f"Monedas          : {p['monedas']}")
    print(f"Idiomas          : {p['idiomas']}")
    print(f"Zonas horarias   : {p['zonas_horarias']}")
    print(f"Bandera (png)    : {p['bandera_png']}")
    print(f"Mapa (Google)    : {p['mapa_google']}")

def menu_paises():
    service = ApiPaisesService()

    while True:
        print("\n==============================")
        print("            Países")
        print("==============================")
        print("1) Buscar país por nombre")
        print("2) Buscar país por código ISO (CL / CHL)")
        print("3) Listar países por región")
        print("0) Volver")
        op = input("Opción: ").strip()

        if op == "1":
            nombre = input("Nombre del país (puede ser parcial, ej. 'chi'): ").strip()
            full = input("Coincidencia exacta? (s/n): ").strip().lower() == "s"
            paises = service.buscar_por_nombre(nombre, full=full)
            if not paises:
                print("❌ No se encontraron países.")
                _pausar(); continue

            # Si hay varios, listar breve y permitir elegir uno para detalle
            print("\nResultados:")
            to_show = min(20, len(paises))
            for i in range(to_show):
                p = paises[i]
                print(f"{i+1:>2}) {p['nombre_comun']} ({p['codigo_cca3']}) - {p['region']}")

            elegido = input("\nVer detalle de (número) o ENTER para omitir: ").strip()
            if elegido:
                try:
                    idx = int(elegido)
                    if 1 <= idx <= to_show:
                        _imprimir_detalle(paises[idx-1])
                except ValueError:
                    pass
            _pausar()

        elif op == "2":
            codigo = input("Código ISO (alpha-2 o alpha-3) ej: CL o CHL: ").strip()
            p = service.buscar_por_codigo(codigo)
            if not p:
                print("❌ No se encontró el país.")
            else:
                _imprimir_detalle(p)
            _pausar()

        elif op == "3":
            print("\nRegiones válidas: Africa, Americas, Asia, Europe, Oceania, Antarctic")
            region = input("Región: ").strip()
            paises = service.listar_por_region(region)
            if not paises:
                print("❌ Sin resultados para esa región.")
                _pausar(); continue

            print(f"\n--- Países en {region} ---")
            for p in paises[:50]:
                print(f"- {p['nombre_comun']} ({p['codigo_cca3']}) | Capital: {p['capital']} | Pob: {p['poblacion']:,}")
            _pausar()

        elif op == "0":
            break
        else:
            print("Opción no válida.")
            _pausar()
