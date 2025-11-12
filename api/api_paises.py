# aplicacion/api_paises.py
# ==============================================================
# Consumo de API pública de países (REST Countries v3)
# - https://restcountries.com/
# - Endpoints usados:
#     /v3.1/name/{name}
#     /v3.1/alpha/{code}
#     /v3.1/region/{region}
# ==============================================================

import requests

BASE_URL = "https://restcountries.com/v3.1"


def _parse_currencies(currencies_obj) -> str:
    """
    currencies_obj = {
      "CLP": {"name": "Chilean peso", "symbol": "$"},
      "USD": {"name": "United States dollar", "symbol": "$"}
    }
    -> "CLP (Chilean peso, $); USD (United States dollar, $)"
    """
    if not isinstance(currencies_obj, dict):
        return "-"
    partes = []
    for code, data in currencies_obj.items():
        nombre = data.get("name", "")
        simbolo = data.get("symbol", "")
        if nombre and simbolo:
            partes.append(f"{code} ({nombre}, {simbolo})")
        elif nombre:
            partes.append(f"{code} ({nombre})")
        else:
            partes.append(code)
    return "; ".join(partes) if partes else "-"


def _parse_languages(langs_obj) -> str:
    """
    langs_obj = {"spa": "Spanish", "eng": "English"} -> "Spanish, English"
    """
    if not isinstance(langs_obj, dict):
        return "-"
    vals = [v for v in langs_obj.values() if isinstance(v, str)]
    return ", ".join(vals) if vals else "-"


def _normalize_country(c: dict) -> dict:
    name = c.get("name", {}) or {}
    capital = c.get("capital", []) or []
    flags = c.get("flags", {}) or {}
    currencies = _parse_currencies(c.get("currencies"))
    languages = _parse_languages(c.get("languages"))
    timezones = c.get("timezones", []) or []

    return {
        "nombre_comun": name.get("common", "-"),
        "nombre_oficial": name.get("official", "-"),
        "codigo_cca2": c.get("cca2", "-"),
        "codigo_cca3": c.get("cca3", "-"),
        "region": c.get("region", "-"),
        "subregion": c.get("subregion", "-"),
        "capital": ", ".join(capital) if capital else "-",
        "poblacion": c.get("population", 0),
        "area_km2": c.get("area", 0),
        "monedas": currencies,
        "idiomas": languages,
        "zonas_horarias": ", ".join(timezones) if timezones else "-",
        "bandera_png": flags.get("png", "-"),
        "bandera_svg": flags.get("svg", "-"),
        "mapa_google": (c.get("maps", {}) or {}).get("googleMaps", "-"),
    }


class ApiPaisesService:
    HEADERS = {"User-Agent": "AppConsole/1.0"}

    def _get(self, path: str, params: dict | None = None):
        url = f"{BASE_URL}{path}"
        try:
            resp = requests.get(url, params=params or {}, headers=self.HEADERS, timeout=8)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout:
            print(" Error: Tiempo de espera agotado al consultar la API.")
        except requests.exceptions.HTTPError as e:
            # 404, etc.
            if e.response is not None and e.response.status_code == 404:
                return None
            print(f" Error HTTP: {e}")
        except requests.exceptions.ConnectionError:
            print("🌐 Error: No hay conexión a Internet o la API no responde.")
        except Exception as e:
            print(f" Error inesperado al consultar API: {e}")
        return None

    # --------- Métodos públicos ----------

    def buscar_por_nombre(self, nombre: str, full: bool = False) -> list[dict]:
        """
        Busca países por nombre. Puede retornar varios.
        full=False -> coincide parcial ('chi' encuentra 'Chile'/'China')
        """
        if not nombre or not isinstance(nombre, str):
            return []
        params = {"fullText": "true"} if full else None
        data = self._get(f"/name/{nombre.strip()}", params)
        if not data or not isinstance(data, list):
            return []
        return [_normalize_country(c) for c in data]

    def buscar_por_codigo(self, codigo: str) -> dict | None:
        """
        Busca país por código ISO, ej: "CL" o "CHL".
        """
        if not codigo or not isinstance(codigo, str):
            return None
        data = self._get(f"/alpha/{codigo.strip()}")
        if not data:
            return None
        # /alpha/{code} puede devolver obj o lista. Normalizamos.
        if isinstance(data, dict):
            # v3.1 retorna un objeto con 'name', etc.
            return _normalize_country(data)
        if isinstance(data, list) and data:
            return _normalize_country(data[0])
        return None

    def listar_por_region(self, region: str) -> list[dict]:
        """
        Lista países por región: Africa, Americas, Asia, Europe, Oceania, Antarctic
        """
        if not region or not isinstance(region, str):
            return []
        data = self._get(f"/region/{region.strip()}")
        if not data or not isinstance(data, list):
            return []
        return [_normalize_country(c) for c in data]
