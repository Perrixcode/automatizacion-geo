"""Extrae una lista literal anterior sin ejecutar código ni imprimir sus valores."""

import argparse
import ast
import json
import os
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from configuracion import ErrorConfiguracion, RUTA_EXCLUSIONES, validar_exclusiones


def extraer_exclusiones(codigo):
    try:
        arbol = ast.parse(codigo)
        asignaciones = [
            nodo for nodo in arbol.body
            if isinstance(nodo, ast.Assign)
            and any(isinstance(destino, ast.Name) and destino.id == "identificadores_excluidos"
                    for destino in nodo.targets)
        ]
        if len(asignaciones) != 1:
            raise ValueError
        valores = ast.literal_eval(asignaciones[0].value)
    except (SyntaxError, ValueError, TypeError, RecursionError):
        raise ErrorConfiguracion("La versión anterior no contiene una única lista literal de exclusiones.") from None
    return validar_exclusiones({"identificadores_excluidos": valores})


def guardar_exclusiones(valores, destino=RUTA_EXCLUSIONES):
    valores = validar_exclusiones({"identificadores_excluidos": valores})
    destino = Path(destino)
    descriptor = None
    try:
        destino.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        # O_EXCL evita sobrescribir archivos y rechaza enlaces simbólicos existentes.
        descriptor = os.open(destino, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as archivo:
            descriptor = None
            json.dump({"identificadores_excluidos": valores}, archivo, ensure_ascii=False, indent=2)
            archivo.write("\n")
    except FileExistsError:
        raise ErrorConfiguracion("La configuración privada ya existe; no se modificó.") from None
    except (OSError, UnicodeError):
        raise ErrorConfiguracion("No se pudo guardar la configuración privada. Revisa el archivo local antes de reintentar.") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origen", type=Path, required=True,
                        help="Copia privada local anterior de main.py, que solo se leerá")
    args = parser.parse_args()
    try:
        try:
            codigo = args.origen.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            raise ErrorConfiguracion("No se pudo leer la copia local anterior.") from None
        guardar_exclusiones(extraer_exclusiones(codigo))
    except ErrorConfiguracion as error:
        print(str(error), file=sys.stderr)
        return 1
    print("Configuración privada creada. No se mostraron identificadores ni se modificó el historial.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
