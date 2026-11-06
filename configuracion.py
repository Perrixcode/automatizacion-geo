"""Carga local de exclusiones sin identificadores personales en el código."""

import json
from pathlib import Path


RAIZ_PROYECTO = Path(__file__).resolve().parent
RUTA_EXCLUSIONES = RAIZ_PROYECTO / "private" / "identificadores_excluidos.json"


class ErrorConfiguracion(ValueError):
    """Error seguro: no incluye contenido del archivo ni identificadores."""


def validar_exclusiones(documento):
    if not isinstance(documento, dict) or set(documento) != {"identificadores_excluidos"}:
        raise ErrorConfiguracion("La configuración debe contener solo identificadores_excluidos.")
    valores = documento["identificadores_excluidos"]
    if not isinstance(valores, list):
        raise ErrorConfiguracion("identificadores_excluidos debe ser una lista de textos.")
    if any(not isinstance(valor, str) or not valor or valor != valor.strip() for valor in valores):
        raise ErrorConfiguracion("Cada exclusión debe ser un texto no vacío y sin espacios exteriores.")
    if "IDENTIFICADOR_PRIVADO_RETIRADO" in valores:
        raise ErrorConfiguracion("La configuración contiene un marcador saneado; usa la configuración privada original.")
    if len(set(valores)) != len(valores):
        raise ErrorConfiguracion("La lista de exclusiones contiene duplicados.")
    # No normalizar: la comparación de pandas conserva la igualdad exacta anterior.
    return valores.copy()


def cargar_identificadores_excluidos(ruta=None):
    ruta = RUTA_EXCLUSIONES if ruta is None else Path(ruta)
    try:
        with ruta.open(encoding="utf-8") as archivo:
            documento = json.load(archivo)
    except FileNotFoundError:
        raise ErrorConfiguracion(
            "Falta private/identificadores_excluidos.json. Migra la configuración anterior "
            "o configura explícitamente las exclusiones según el README. No se procesaron datos."
        ) from None
    except (OSError, UnicodeError, ValueError):
        raise ErrorConfiguracion("No se pudo leer una configuración JSON válida de exclusiones.") from None
    return validar_exclusiones(documento)
