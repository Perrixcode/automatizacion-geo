# Automatización GEO

Prototipo en desarrollo con **Python, pandas y openpyxl** para procesar asistencia desde archivos Excel de GeoVictoria, un maestro de trabajadores y un cronograma mensual.

El proyecto nace de un proceso operacional que requiere limpiar datos, revisar marcaciones y preparar información para Zenda. La estimación inicial del proceso manual fue de 3 a 4 horas por período; **no es una medición de ahorro conseguida por este programa**.

## Estado del proyecto

El código ya contiene lectura y cruce de las tres fuentes, validaciones, cálculo de programación semanal, clasificación parcial de incidencias y análisis de colaciones. Es un prototipo de consola: esas piezas no acreditan un flujo mensual completo ni un cálculo laboral validado para uso definitivo.

La exportación final para Zenda, la cobertura integral de reglas y una demostración reproducible del flujo completo con datos ficticios siguen pendientes. No hay conexión API con GeoVictoria o Zenda ni envío automático de información.

## Qué está implementado en el código

- Lectura del maestro y cronograma; detección de duplicados, campos faltantes, estados y jornadas inconsistentes.
- Cruce del cronograma con el maestro, cálculo de horas netas programadas y agrupación semanal.
- Lectura del Excel de GeoVictoria y relación con el maestro mediante identificadores.
- Cruce de programación y marcaciones por trabajador y fecha.
- Clasificación parcial de marcaciones incompletas y algunos patrones de ajuste, conservando columnas originales y ajustadas por separado.
- Clasificación de ciertos casos como pendientes de revisión, sin resolver todos los patrones posibles.
- Cálculo de duración bruta de jornadas y colaciones, estadísticas descriptivas y posibles valores atípicos mediante IQR.
- Exclusiones configuradas en un archivo privado local, sin identificadores personales incorporados en el código actual.

La detección de una inconsistencia no significa que todas las rutas del programa bloqueen automáticamente los cálculos posteriores. Las reglas de ajuste son parte del prototipo y requieren revisión operativa; no sustituyen una validación laboral ni autorizan pagos o descuentos.

## Qué falta completar y validar

- Fixtures ficticios para ejecutar el procesamiento completo sin archivos privados.
- Pruebas automatizadas de las reglas de negocio y de sus casos límite.
- Resolución integral de incidencias y tratamiento de jornadas especiales.
- Cálculo final validado de horas trabajadas, extraordinarias, descuentos, feriados, ausencias, licencias y vacaciones.
- Resumen mensual y exportación final compatible con el proceso de Zenda.
- Modularización del script principal e interfaz de ejecución más clara.

El archivo `prueba_colacion.py` contiene ejemplos exploratorios impresos en consola, no una suite de pruebas con aserciones. Las pruebas agregadas en `tests/` cubren la configuración privada y su migración; **no validan todavía el motor completo de asistencia**.

## Fuentes y ejecución

El script espera estos archivos privados en `datos/`:

- `maestro_trabajadores.xlsx`: identificadores, tipo de jornada, referencia semanal, área, estado activo y reglas asociadas.
- `cronograma_mensual.xlsx`: trabajador, fecha, estado y horarios programados.
- `geovictoria.xlsx`: export de marcaciones con el formato que utiliza el script; se lee con `header=1`.

No se incluyen esos Excel en el repositorio. Instalar dependencias no proporciona una demo ejecutable del flujo completo.

```sh
git clone https://github.com/Perrixcode/automatizacion-geo.git
cd automatizacion-geo
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Antes de ejecutar, configura las exclusiones según la sección siguiente y revisa los formatos de entrada. Desde la raíz del proyecto:

```sh
python3 main.py
```

El resultado actual se inspecciona en consola. No se genera todavía el archivo mensual final para Zenda. La salida puede mostrar información de los Excel privados: no publiques capturas ni logs de una ejecución con datos reales.

## Configuración privada de exclusiones

`main.py` carga `private/identificadores_excluidos.json` antes de leer los Excel. La ruta se resuelve respecto del proyecto, no del directorio desde el que se invoca Python.

El archivo debe contener un objeto con una única clave, `identificadores_excluidos`, cuyo valor sea una lista de textos. Se conserva la comparación exacta anterior de pandas: no se cambian mayúsculas, puntuación ni formato de los identificadores.

Si el archivo falta, es inválido o contiene valores duplicados, el programa se detiene. **No se supone una lista vacía**, porque eso podría volver a incluir registros que deben quedar fuera. Una lista vacía explícita es válida solo si se ha revisado que no corresponde excluir a nadie.

### Conservar una configuración privada existente

Si ya tienes `private/identificadores_excluidos.json`, consérvalo al cambiar de clon. No lo sobrescribas con la plantilla vacía y no lo añadas a Git. El programa mantiene los valores exactos del archivo privado.

Si todavía necesitas extraer la lista desde una copia privada anterior de `main.py`, puedes ejecutar una vez:

```sh
python3 scripts/migrar_exclusiones.py --origen /ruta/local/main-anterior.py
```

El script lee esa copia con AST, sin ejecutarla ni mostrar identificadores, y crea el JSON privado sin sobrescribir archivos existentes. No admite recuperar versiones por SHA: el historial saneado contiene un marcador, no una configuración operativa. Tanto la carga como el migrador rechazan ese marcador.

El archivo nuevo se crea con permisos de lectura y escritura para su propietario en sistemas POSIX. Comprueba que queda ignorado por Git:

```sh
git check-ignore private/identificadores_excluidos.json
```

No mezcles ni publiques ramas del historial anterior. Tras una limpieza histórica, utiliza un clon nuevo y restaura únicamente la configuración privada y los datos operacionales que correspondan.

### Instalación nueva

La plantilla `config/identificadores_excluidos.example.json` contiene una lista vacía y ningún dato personal. Úsala únicamente tras decidir explícitamente las exclusiones que corresponden. Crea `private/identificadores_excluidos.json` localmente y no incorpores sus valores al código, a pruebas ni a commits.

## Pruebas de configuración

```sh
python3 -m unittest discover -s tests -v
python3 -m compileall -q main.py configuracion.py scripts tests
```

Las pruebas usan identificadores ficticios. Cubren carga, validación, errores sin revelar contenido, migración sin ejecutar código, conservación de valores y protección frente a sobrescritura. Si pandas está instalado, comprueban también que la exclusión conserva la igualdad exacta del filtro anterior.

Estas verificaciones son acotadas. No acreditan la exactitud de cálculos laborales ni una ejecución completa con los Excel operacionales.

## Privacidad y límites

- Los Excel operacionales y salidas Excel están excluidos mediante `.gitignore`.
- La carpeta `private/` está excluida de Git y no forma parte de la distribución pública.
- El código actual no incorpora la lista personal de exclusiones anterior.
- `.gitignore` no protege un archivo ya versionado, un `git add -f`, capturas, logs ni copias externas.
- El saneamiento histórico reemplaza el identificador por un marcador en las versiones alcanzables. No elimina copias externas, respaldos privados ni garantiza la purga de objetos o vistas conservados por GitHub. Esa limpieza residual requiere una revisión separada con GitHub Support.

## Autor

**Esteban Iturra Camaño**

Proyecto de formación en Python, análisis de datos y automatización de procesos, aplicado a un problema operacional real.
