# Automatización GEO

Sistema en desarrollo para automatizar el procesamiento de asistencia laboral a partir de registros exportados desde GeoVictoria, cronogramas de trabajo y reglas operacionales.

El proyecto nace de un proceso real que actualmente requiere varias horas de trabajo manual cada mes para limpiar datos, revisar marcaciones, calcular jornadas y preparar información para su posterior procesamiento en Zenda.

> 🚧 Proyecto actualmente en desarrollo.

## 🎯 Objetivo

Automatizar el flujo de procesamiento de asistencia, reduciendo tareas manuales y aumentando la trazabilidad de los cálculos.

El sistema busca transformar:

GeoVictoria + Cronograma + Reglas de negocio

en:

- horas trabajadas;
- horas programadas;
- incidencias de marcación;
- horas extraordinarias;
- horas de descuento;
- horas trabajadas en feriados;
- ausencias;
- licencias;
- vacaciones;
- resumen mensual por trabajador;
- información preparada para su posterior carga en Zenda.

## 🧩 Problema que resuelve

Actualmente el proceso requiere:

1. Descargar un archivo Excel desde GeoVictoria.
2. Eliminar columnas que no son necesarias.
3. Revisar manualmente marcaciones incompletas o desplazadas.
4. Comparar las marcaciones con el cronograma de cada trabajador.
5. Calcular horas diarias y semanales.
6. Identificar diferencias respecto de la jornada correspondiente.
7. Separar horas extra y descuentos.
8. Procesar manualmente feriados, ausencias, permisos, licencias y vacaciones.
9. Consolidar la información mensual para Zenda.

Este proceso puede requerir aproximadamente 3 a 4 horas de trabajo manual por período.

## ⚙️ Tecnologías

- Python
- pandas
- openpyxl
- datetime
- Excel
- Git
- GitHub

## 📥 Fuentes de datos

Actualmente el proyecto utiliza tres fuentes principales.

### Maestro de trabajadores

Contiene información relativamente estable de cada trabajador:

- identificador;
- tipo de jornada;
- horas de referencia semanal;
- área;
- estado activo;
- derechos laborales que afectan el cálculo.

### Cronograma mensual

Representa la planificación real de trabajo:

- fecha;
- trabajador;
- estado programado;
- entrada programada;
- salida programada;
- colación programada;
- observaciones.

### GeoVictoria

Se utiliza como fuente de marcaciones reales de asistencia.

Del archivo original se utilizan principalmente:

- identificador;
- fecha;
- hora de ingreso;
- inicio de colación;
- fin de colación;
- hora de salida.

GeoVictoria se utiliza actualmente únicamente como medio de registro de asistencia. La planificación de turnos, licencias, permisos y otras novedades se administra fuera de la plataforma.

## ✅ Funcionalidades implementadas

Actualmente el proyecto ya permite:

- importar el maestro de trabajadores;
- importar el cronograma mensual;
- validar identificadores duplicados;
- validar tipos de jornada;
- detectar información obligatoria faltante;
- validar coherencia de derechos asociados al trabajador;
- detectar turnos duplicados;
- validar estados de programación;
- detectar días libres con horarios cargados;
- detectar días de trabajo sin horarios;
- validar colaciones programadas;
- detectar trabajadores inexistentes en el maestro;
- relacionar cronograma y maestro mediante `merge`;
- detectar trabajadores inactivos programados;
- validar coherencia entre entrada y salida;
- calcular horas netas programadas;
- agrupar jornadas por semana;
- calcular días programados;
- considerar horas computables asociadas a derechos laborales;
- comparar la programación semanal con la referencia correspondiente;
- detectar semanas con programación desajustada.

## 🔍 Validación de datos

El proyecto utiliza validaciones antes de realizar los cálculos.

Ejemplos:

- un trabajador no puede aparecer dos veces el mismo día;
- un día marcado como libre no debe contener horario;
- un día de trabajo debe contener entrada y salida;
- un trabajador inactivo no debe tener turnos programados;
- las colaciones programadas deben utilizar valores permitidos;
- todos los identificadores del cronograma deben existir en el maestro;
- los trabajadores full-time deben cumplir su referencia semanal considerando las reglas aplicables.

El objetivo es detectar inconsistencias antes de que los datos incorrectos lleguen al cálculo final.

## 🧮 Procesamiento semanal

Las horas programadas se calculan a partir de:

```text
hora salida
-
hora entrada
-
colación programada
=
horas netas programadas
```

Posteriormente las jornadas son agrupadas por trabajador y semana.

```text
horas diarias
        ↓
agrupación semanal
        ↓
horas programadas
        ↓
reglas computables
        ↓
comparación con referencia semanal
```

Esto permite detectar automáticamente diferencias en la programación.

## 🚨 Incidencias

Una parte importante del proyecto será diferenciar entre:

- datos válidos;
- ajustes automáticos;
- situaciones que requieren revisión humana.

Estados considerados:

```text
OK
AJUSTADO AUTOMÁTICAMENTE
REQUIERE REVISIÓN
```

El programa no pretende inventar información cuando una marcación es ambigua.

Cuando no sea posible determinar correctamente lo ocurrido, el caso será enviado a revisión antes de generar el cálculo definitivo.

## 🗺️ Flujo objetivo

```text
Maestro trabajadores
        +
Cronograma mensual
        +
GeoVictoria
        ↓
Validación de datos
        ↓
Cruce de información
        ↓
Detección de incidencias
        ↓
Revisión / resolución
        ↓
Cálculo diario
        ↓
Cálculo semanal
        ↓
Horas extra / descuentos
        ↓
Feriados / ausencias / licencias / vacaciones
        ↓
Resumen mensual
        ↓
Excel preparado para procesamiento en Zenda
```

## 🚧 Roadmap

### MVP

- [x] Maestro de trabajadores
- [x] Cronograma mensual
- [x] Validaciones básicas
- [x] Cálculo de horas programadas
- [x] Agrupación semanal
- [x] Validación de programación semanal
- [ ] Integración del procesamiento de GeoVictoria
- [ ] Cruce entre horas programadas y marcaciones reales
- [ ] Motor de incidencias
- [ ] Cálculo de horas reales
- [ ] Feriados
- [ ] Ausencias
- [ ] Licencias y vacaciones
- [ ] Horas extraordinarias
- [ ] Horas de descuento
- [ ] Resumen mensual
- [ ] Exportación final a Excel

### Futuras mejoras

- Integración mediante API con GeoVictoria.
- Evaluar integración con Zenda.
- Generación automática del cronograma base.
- Dashboard de resultados.
- Interfaz gráfica.
- Pruebas automatizadas.
- Mayor modularización del proyecto.

## 🔐 Privacidad

El proyecto fue desarrollado utilizando información operacional real.

Por motivos de privacidad:

- los archivos Excel reales no forman parte del repositorio;
- los datos personales de trabajadores están excluidos mediante `.gitignore`;
- los archivos generados por el sistema tampoco se versionan.

Para una versión pública del proyecto se utilizarán posteriormente datos ficticios de ejemplo.

## 📦 Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Perrixcode/automatizacion-geo.git
cd automatizacion-geo
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en macOS/Linux:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 📌 Estado del proyecto

El proyecto se encuentra actualmente en desarrollo activo.

La prioridad actual es completar el motor de cálculo y validación utilizando archivos Excel. Una vez alcanzado el MVP, se evaluará reemplazar la importación manual desde GeoVictoria por una integración mediante API.

## 👨‍💻 Autor

**Esteban Iturra Camaño**

Proyecto desarrollado como parte de mi formación en Python, análisis de datos y automatización de procesos, aplicando programación a un problema operacional real.