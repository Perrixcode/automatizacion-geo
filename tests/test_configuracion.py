import ast
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from configuracion import ErrorConfiguracion, cargar_identificadores_excluidos, validar_exclusiones
from scripts.migrar_exclusiones import extraer_exclusiones, guardar_exclusiones, leer_version_git


RAIZ = Path(__file__).resolve().parents[1]


class PruebasConfiguracion(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.ruta = Path(self.temporal.name) / "private" / "identificadores_excluidos.json"

    def test_roundtrip_conserva_texto_orden_y_copia(self):
        valores = ["DEMO-A", "demo-b"]
        guardar_exclusiones(valores, self.ruta)
        resultado = cargar_identificadores_excluidos(self.ruta)
        self.assertEqual(resultado, valores)
        resultado.append("DEMO-C")
        self.assertEqual(cargar_identificadores_excluidos(self.ruta), valores)

    def test_lista_vacia_explicita_es_valida(self):
        guardar_exclusiones([], self.ruta)
        self.assertEqual(cargar_identificadores_excluidos(self.ruta), [])

    def test_ausente_no_equivale_a_lista_vacia(self):
        with self.assertRaisesRegex(ErrorConfiguracion, "Falta private/"):
            cargar_identificadores_excluidos(self.ruta)

    def test_json_invalido_no_filtra_contenido(self):
        self.ruta.parent.mkdir()
        self.ruta.write_text('{"DEMO-PRIVADO":', encoding="utf-8")
        with self.assertRaises(ErrorConfiguracion) as error:
            cargar_identificadores_excluidos(self.ruta)
        self.assertNotIn("DEMO-PRIVADO", str(error.exception))

    def test_codificacion_invalida_se_rechaza(self):
        self.ruta.parent.mkdir()
        self.ruta.write_bytes(b"\xff")
        with self.assertRaises(ErrorConfiguracion):
            cargar_identificadores_excluidos(self.ruta)

    def test_directorio_no_es_configuracion(self):
        self.ruta.mkdir(parents=True)
        with self.assertRaises(ErrorConfiguracion):
            cargar_identificadores_excluidos(self.ruta)

    def test_esquemas_invalidos_se_rechazan(self):
        for documento in ([], None, {}, {"otra": []}, {"identificadores_excluidos": [], "extra": 1}):
            with self.subTest(documento=documento), self.assertRaises(ErrorConfiguracion):
                validar_exclusiones(documento)

    def test_lista_y_elementos_invalidos_se_rechazan(self):
        for valores in ("DEMO-A", None, [1], [True], [None], [""], [" DEMO-A"], ["DEMO-A "]):
            with self.subTest(valores=valores), self.assertRaises(ErrorConfiguracion):
                validar_exclusiones({"identificadores_excluidos": valores})

    def test_duplicados_se_rechazan(self):
        with self.assertRaises(ErrorConfiguracion):
            validar_exclusiones({"identificadores_excluidos": ["DEMO-A", "DEMO-A"]})

    def test_error_de_validacion_no_filtra_valor(self):
        with self.assertRaises(ErrorConfiguracion) as error:
            validar_exclusiones({"identificadores_excluidos": [" DEMO-PRIVADO"]})
        self.assertNotIn("DEMO-PRIVADO", str(error.exception))

    def test_no_sobrescribe_configuracion_existente(self):
        guardar_exclusiones(["DEMO-A"], self.ruta)
        original = self.ruta.read_bytes()
        with self.assertRaises(ErrorConfiguracion):
            guardar_exclusiones(["DEMO-B"], self.ruta)
        self.assertEqual(self.ruta.read_bytes(), original)

    @unittest.skipIf(os.name == "nt", "Permisos POSIX")
    def test_archivo_privado_desde_su_creacion(self):
        guardar_exclusiones(["DEMO-A"], self.ruta)
        self.assertEqual(self.ruta.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.ruta.parent.stat().st_mode & 0o777, 0o700)

    @unittest.skipIf(os.name == "nt", "Enlace simbólico POSIX")
    def test_no_sigue_enlace_simbolico_existente(self):
        self.ruta.parent.mkdir()
        otro = self.ruta.parent / "otro.json"
        otro.write_text("NO MODIFICAR", encoding="utf-8")
        self.ruta.symlink_to(otro)
        with self.assertRaises(ErrorConfiguracion):
            guardar_exclusiones(["DEMO-A"], self.ruta)
        self.assertEqual(otro.read_text(encoding="utf-8"), "NO MODIFICAR")

    def test_migracion_extrae_sin_ejecutar_fuente(self):
        codigo = 'raise RuntimeError("NO EJECUTAR")\nidentificadores_excluidos = ["DEMO-A", "DEMO-B"]\n'
        self.assertEqual(extraer_exclusiones(codigo), ["DEMO-A", "DEMO-B"])

    def test_migracion_rechaza_codigo_dinamico_ambiguo_o_invalido(self):
        fuentes = (
            "identificadores_excluidos = funcion()",
            "identificadores_excluidos = []\nidentificadores_excluidos = []",
            "def funcion():\n    identificadores_excluidos = []",
            "identificadores_excluidos = [",
            "otra_lista = []",
            "identificadores_excluidos = [1]",
        )
        for fuente in fuentes:
            with self.subTest(fuente=fuente), self.assertRaises(ErrorConfiguracion):
                extraer_exclusiones(fuente)

    def test_ref_git_rechaza_opciones_y_rutas(self):
        with patch("scripts.migrar_exclusiones.subprocess.run") as ejecutar:
            for referencia in ("--help", "HEAD", "abc123", "abc1234:otro", "../archivo"):
                with self.subTest(referencia=referencia), self.assertRaises(ErrorConfiguracion):
                    leer_version_git(referencia)
            ejecutar.assert_not_called()

    def test_git_lee_solo_main_del_commit_local(self):
        fuente = 'identificadores_excluidos = ["DEMO-A"]'
        with patch("scripts.migrar_exclusiones.subprocess.run", return_value=subprocess.CompletedProcess([], 0, fuente)) as ejecutar:
            self.assertEqual(leer_version_git("abcdef1", Path(self.temporal.name)), fuente)
        self.assertEqual(ejecutar.call_args.args[0], ["git", "show", "abcdef1:main.py"])
        self.assertTrue(ejecutar.call_args.kwargs["capture_output"])

    def test_error_git_no_filtra_stderr(self):
        fallo = subprocess.CalledProcessError(1, "git", stderr="DEMO-PRIVADO")
        with patch("scripts.migrar_exclusiones.subprocess.run", side_effect=fallo):
            with self.assertRaises(ErrorConfiguracion) as error:
                leer_version_git("abcdef1")
        self.assertNotIn("DEMO-PRIVADO", str(error.exception))

    def test_migracion_y_carga_no_imprimen_identificadores(self):
        salida, errores = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            guardar_exclusiones(extraer_exclusiones('identificadores_excluidos = ["DEMO-PRIVADO"]'), self.ruta)
            cargar_identificadores_excluidos(self.ruta)
        self.assertEqual(salida.getvalue() + errores.getvalue(), "")

    def test_filtro_conserva_igualdad_exacta(self):
        try:
            import pandas as pd
        except ImportError:
            self.skipTest("Instalar requirements.txt para comprobar el filtro pandas")
        guardar_exclusiones(["DEMO-A"], self.ruta)
        serie = pd.Series(["DEMO-A", "DEMO-B", "demo-a", None])
        anterior = serie.isin(["DEMO-A"])
        nuevo = serie.isin(cargar_identificadores_excluidos(self.ruta))
        self.assertTrue(anterior.equals(nuevo))
        self.assertEqual(serie[~nuevo].tolist(), ["DEMO-B", "demo-a", None])

    def test_carga_antes_de_leer_excel_y_sin_lista_literal(self):
        codigo = (RAIZ / "main.py").read_text(encoding="utf-8")
        arbol = ast.parse(codigo)
        llamadas = [nodo for nodo in ast.walk(arbol) if isinstance(nodo, ast.Call)]
        linea_carga = next(n.lineno for n in llamadas if isinstance(n.func, ast.Name) and n.func.id == "cargar_identificadores_excluidos")
        lecturas = [n.lineno for n in llamadas if isinstance(n.func, ast.Attribute) and n.func.attr == "read_excel"]
        self.assertTrue(lecturas)
        self.assertLess(linea_carga, min(lecturas))
        with self.assertRaises(ErrorConfiguracion):
            extraer_exclusiones(codigo)

    def test_ruta_predeterminada_no_depende_del_directorio_actual(self):
        import configuracion
        self.assertEqual(configuracion.RUTA_EXCLUSIONES, RAIZ / "private" / "identificadores_excluidos.json")


if __name__ == "__main__":
    unittest.main()
