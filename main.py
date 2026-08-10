import pandas as pd #Llamo al directorio pandas y lo abrevio como pd
import openpyxl # Llamo al directorio openpyxl
import datetime

#FUNCIONES USADAS PARA CONSTRUIR LOS DATOS

"""print(datos[["Fecha", "fecha"]].head(30))
print(
    datos[datos["Fecha"].str.endswith("(F)")]["Fecha"].head(10)
)

print(datos.head()) #-> Muestro las primeras 5 filas de los nuevos datos

print(datos.head())
print(datos.columns.tolist()) #variable.columns -> Llama a mostrar los nombres de las columnas y .tolist() -> Los muestra en formato de lista
print(datos.iloc[0]) # iloc -> selecciona la primera fila de datos [] -> le doy posicion"
datos.info() #Muestra info detallada del dataframe, no es necesario printear 
print(datos.isna().sum())#Isna: Valor vacio, responde en bool / .sum suma los valores de cada columna
print(cantidad_marcaciones.value_counts().sort_index()) # value_counts() cuenta cada valor sort_index ordena como lista 
print(marcaciones_incompletas.sum()) #-> Me muestra  cantidad de al menos una celda vacia por fila en forma horizontal y descontando aquellas que tengan las 4 vacias 
print(
    incidencias[
        [
            "Apellidos",
            "Nombre",
            "Fecha",
            "hora_ingreso",
            "inicio_colacion",
            "fin_colacion",
            "hora_salida",
        ]
    ].head(420).to_string(index=False) #.tostring convierte la tabla en texto, evitando los puntos suspensivos intermedios / index=False oculta los indices
)
print(  
    filas_una_marcacion[
    [
        "Apellidos",
        "Nombre",
        "Fecha",
        "hora_ingreso",
        "inicio_colacion",
        "fin_colacion",
        "hora_salida"
    ]
].to_string(index=False)
)
print(sin_marcaciones.sum())

print(
    datos[datos["es_feriado"]][
        ["Fecha", "fecha", "es_feriado"]
    ].drop_duplicates() #Printea las 3 columnas con aquellas fechas terminadas en (F) y elimina los duplicados con drop.duplicates
)

print(
    datos[posible_salida_desplazada][
        [
            "Apellidos",
            "Nombre",
            "Fecha",
            "fecha",
            "hora_salida"
        ]
    ].to_string(index=False)
)

print(
    candidatas_salida[
        [
            "Nombre",
            "fecha",
            "fecha_jornada_anterior",
            "hora_salida"
        ]
    ].to_string(index=False)
)


"""

#INICIO ESTRICTO DEL PROGRAMA 

print("AUTOMATIZACIÓN GEO")

ruta_maestro = pd.read_excel("datos/maestro_trabajadores.xlsx")
#print(ruta_maestro.head())

ids_duplicados = ruta_maestro["trabajador_id"].duplicated() #Verificamos ids duplicados
#print(ids_duplicados.sum())

#Creacion de columnas obligatorias como listas
columnas_obligatorias = ["trabajador_id", "nombre", "tipo_jornada", "area", "derecho_alimentacion", "minutos_derecho_alimentacion", "activo"]

#print(ruta_maestro[columnas_obligatorias].isna().sum()) # Validando que las columnas obligatorias estén con información

#print(ruta_maestro.columns.to_list())
full_time = ruta_maestro[
        ruta_maestro["tipo_jornada"] == "full_time"
]
#print(full_time[["nombre", "tipo_jornada", "horas_referencia_semanal"]])

sin_hora_referencia = full_time["horas_referencia_semanal"].isna().sum()
#print(sin_hora_referencia)

tipos_jornadas_validas = ["full_time", "part_time"] #tipo de jornada valida
jornada_invalida = ~ruta_maestro["tipo_jornada"].isin(tipos_jornadas_validas) # tipo de jornadas invalidads negando el resultado de jornada valida
#print(jornada_invalida.sum())

derecho_inconsistente = (ruta_maestro["derecho_alimentacion"] == False ) & (ruta_maestro["minutos_derecho_alimentacion"] != 0 ) #Verifica que derecho alimentacion al ser falsa debe si o si ser 0, si no es un error
#print(derecho_inconsistente.sum())

derecho_sin_minutos = (ruta_maestro["derecho_alimentacion"] == True) & (ruta_maestro["minutos_derecho_alimentacion"] != 60)
#print(derecho_sin_minutos.sum())

cronograma_mensual = pd.read_excel("datos/cronograma_mensual.xlsx")
#print(cronograma_mensual.columns.to_list()) #muestra nombre de cada columna en formato de lista
#print(cronograma_mensual.dtypes) #dtypes muestra tipo de datos detectado por pandas

#print(cronograma_mensual["entrada_programada"].iloc[0]) #dame el elemento que está en la poscion 0 de esa columna (casilla)
#print(type(cronograma_mensual["entrada_programada"].iloc[0]))

turnos_duplicados = cronograma_mensual.duplicated(
    subset=["fecha", "trabajador_id"],
    keep=False
)

estados_validos = ["trabajo", "libre"]
estado_invalido = ~cronograma_mensual["estado_programado"].isin(estados_validos)
#print(estado_invalido.sum())

libre_con_horario = (cronograma_mensual["estado_programado"] == "libre") & ((cronograma_mensual["entrada_programada"].notna()) | (cronograma_mensual["salida_programada"].notna()))
#print(libre_con_horario.sum())

trabajo_sin_horario = (cronograma_mensual["estado_programado"] == "trabajo") & ((cronograma_mensual["entrada_programada"].isna()) | (cronograma_mensual["salida_programada"].isna()))

#print(trabajo_sin_horario.sum())  
#print(cronograma_mensual[turnos_duplicados])
#print(turnos_duplicados.sum())

#isna = vacio
#notna = contiene dato

libre_con_colacion = (cronograma_mensual["estado_programado"] == "libre") & (cronograma_mensual["colacion_programada_minutos"] != 0)
#print(libre_con_colacion.sum())
#print(cronograma_mensual[libre_con_colacion])

colaciones_validas_programadas = [0, 30, 60]
colacion_programada_invalida = ~(cronograma_mensual["colacion_programada_minutos"].isin(colaciones_validas_programadas)) 
#print(colacion_programada_invalida.sum())

id_invalido = ~(
    cronograma_mensual["trabajador_id"]
    .isin(ruta_maestro["trabajador_id"])
)
#print(id_invalido.sum())

cruce_cronograma_maestro = cronograma_mensual.merge(ruta_maestro[["trabajador_id", "nombre"]], on="trabajador_id", how="left", suffixes=("_cronograma", "_maestro"))
#print(cruce_cronograma_maestro[["trabajador_id", "nombre_cronograma", "nombre_maestro"]].head(10))
    
cronograma_completo = cronograma_mensual.merge(
    ruta_maestro[
        [
            "trabajador_id",
            "tipo_jornada",
            "horas_referencia_semanal",
            "area",
            "derecho_alimentacion",
            "minutos_derecho_alimentacion",
            "activo"
        ]
    ],
    on="trabajador_id",
    how="left"
)
#print(cronograma_completo.head())
#print(cronograma_completo.columns)

merge_sin_coincidencia = cronograma_completo["tipo_jornada"].isna()
#print(merge_sin_coincidencia.sum())

inactivo_con_turno = (cronograma_completo["activo"] == False) & (cronograma_completo["estado_programado"] == "trabajo")
#print(inactivo_con_turno.sum())

turnos_trabajo = cronograma_completo[
    cronograma_completo["estado_programado"] == "trabajo"
].copy()

horario_programado_invalido = turnos_trabajo["salida_programada"] <= turnos_trabajo["entrada_programada"]
#print(horario_programado_invalido.sum())

fecha_prueba = turnos_trabajo["fecha"].iloc[0]
entrada_prueba = turnos_trabajo["entrada_programada"].iloc[0]
salida_prueba = turnos_trabajo["salida_programada"].iloc[0]

inicio_prueba = datetime.datetime.combine(fecha_prueba.date(), entrada_prueba)
fin_prueba = datetime.datetime.combine(fecha_prueba.date(), salida_prueba)
duracion_prueba = fin_prueba - inicio_prueba
#print(inicio_prueba)
#print(fin_prueba)
#print(duracion_prueba)
duracion_segundos = duracion_prueba.total_seconds()
minutos_programados_brutos = duracion_segundos/60
#print(minutos_programados_brutos)

colacion_prueba = turnos_trabajo["colacion_programada_minutos"].iloc[0]
duracion_neta_prueba = minutos_programados_brutos - colacion_prueba
#print(duracion_neta_prueba)
horas_programadas_netas = duracion_neta_prueba / 60
#print(horas_programadas_netas)

#print(cronograma_completo.columns)

def calcular_horas_programadas(fila):
    fecha = fila["fecha"]
    entrada = fila["entrada_programada"]
    salida = fila["salida_programada"]
    colacion = fila["colacion_programada_minutos"]

    inicio = datetime.datetime.combine(fecha, entrada)
    fin = datetime.datetime.combine(fecha, salida)

    duracion = fin - inicio
    segundos_brutos = duracion.total_seconds()
    minutos_brutos = segundos_brutos/60
    minutos_netos = minutos_brutos - colacion
    horas_netas = minutos_netos/60
    return  horas_netas

#print(calcular_horas_programadas(turnos_trabajo.iloc[0])) 

turnos_trabajo["horas_programadas_netas"] = turnos_trabajo.apply(calcular_horas_programadas, axis=1) #Creamos nueva columna y guardamos los datos de la funcion recorriendo por fila allí


"""print(
    turnos_trabajo[
        [
            "nombre",
            "fecha",
            "entrada_programada",
            "salida_programada",
            "colacion_programada_minutos",
            "horas_programadas_netas"
        ]
        
    ].head(20)
)"""

turnos_trabajo["semana"] = (turnos_trabajo["fecha"].dt.to_period("W-SUN"))

"""print(
    turnos_trabajo[[
        "nombre",
        "fecha",
        "semana",
        "horas_programadas_netas"
    ]
].head(20)
)"""

resumen_semanal_programado = turnos_trabajo.groupby(["trabajador_id", "semana", "nombre"])["horas_programadas_netas"].sum()
#print(resumen_semanal_programado)
resumen_semanal_programado = resumen_semanal_programado.reset_index()

resumen_semanal_programado = resumen_semanal_programado.merge(
    ruta_maestro[[
                "trabajador_id",
                "tipo_jornada",
                "horas_referencia_semanal",
                "derecho_alimentacion",
                "minutos_derecho_alimentacion"
        ]
    ],
    on="trabajador_id",
    how="left"
)
#print(resumen_semanal_programado.head(20))

dias_programados = turnos_trabajo.groupby(["trabajador_id", "semana"]).size()
dias_programados = dias_programados.reset_index(name="dias_programados")
#print(dias_programados)

resumen_semanal_programado = resumen_semanal_programado.merge(dias_programados, on= ["trabajador_id", "semana"], how="left")
#resumen_semanal_programado = resumen_semanal_programado.reset_index(drop=True) #drop true crea indice nuevo y bota el antigyo 

#print(resumen_semanal_programado)

resumen_semanal_programado["minutos_derecho_semana"] = resumen_semanal_programado["dias_programados"] * resumen_semanal_programado["minutos_derecho_alimentacion"]
resumen_semanal_programado["horas_derecho_semana"] = resumen_semanal_programado["minutos_derecho_semana"]/60
resumen_semanal_programado["horas_programadas_computables"] = resumen_semanal_programado["horas_derecho_semana"] + resumen_semanal_programado["horas_programadas_netas"]
#print(resumen_semanal_programado)

resumen_semanal_programado["diferencia_programacion"] = resumen_semanal_programado["horas_programadas_computables"] - resumen_semanal_programado["horas_referencia_semanal"]
print(
    resumen_semanal_programado[[
            "trabajador_id",
            "nombre",
            "semana",
            "tipo_jornada",
            "horas_referencia_semanal",
            "horas_programadas_computables",
            "diferencia_programacion"
        ]
    ]
)

programacion_semanal_desajustada = (resumen_semanal_programado["tipo_jornada"]== "full_time") & (resumen_semanal_programado["diferencia_programacion"] != 0)
print(programacion_semanal_desajustada.sum())





"""

datos = pd.read_excel("datos/geovictoria.xlsx", header=1) #header es el numero de fila
datos = datos.rename(columns={ #-> Llamo a datos con funcion .rename para renombrar nombres de columnas
    "Entró": "hora_ingreso",
    "Salió": "inicio_colacion",
    "Entró.1": "fin_colacion",
    "Salió.1": "hora_salida"
})
columnas_utiles = [ #-> Creo lista de las columnas que usaré
    "Apellidos",
    "Nombre",
    "Identificador",
    "Fecha",
    "hora_ingreso",
    "inicio_colacion",
    "fin_colacion",
    "hora_salida",
    "Cargo"
]    
datos = datos[columnas_utiles] #-> Asigno nuevo valor a variable datos

datos["es_feriado"] = datos["Fecha"].str.endswith(" (F)")


fecha_limpia = datos["Fecha"].str.replace(" (F)", "", regex=False)

datos["fecha"] = pd.to_datetime(
    fecha_limpia.str[-10:],
    format="%d-%m-%Y"
)

columnas_marcaciones = [
    "hora_ingreso",
    "inicio_colacion",
    "fin_colacion",
    "hora_salida"
]
cantidad_marcaciones = datos[columnas_marcaciones].notna().sum(axis=1) #.notna El valor no está vacío? responde en booleano / si tiene contenido da true


una_marcacion = cantidad_marcaciones == 1

filas_una_marcacion = datos[una_marcacion]

sin_marcaciones = datos[columnas_marcaciones].isna().all(axis=1) #axis= 0 vertical /axis= 1 horizontal 

marcaciones_incompletas = (
    datos[columnas_marcaciones].isna().any(axis=1)
    & ~sin_marcaciones
)
incidencias = datos[marcaciones_incompletas]

limite_madrugada = pd.Timedelta(hours=6)

posible_salida_desplazada = (
    (cantidad_marcaciones == 1)
    & datos["hora_salida"].notna()
    & (datos["hora_salida"] < limite_madrugada)
)

candidatas_salida = datos[posible_salida_desplazada].copy()
candidatas_salida["fecha_jornada_anterior"] = (
    candidatas_salida["fecha"] - pd.Timedelta(days=1)
)

"""
