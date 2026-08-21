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
"""print(
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
)"""

programacion_semanal_desajustada = (resumen_semanal_programado["tipo_jornada"]== "full_time") & (resumen_semanal_programado["diferencia_programacion"] != 0)
#print(programacion_semanal_desajustada.sum())





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
# PROCESAMIENTO DE MARCACIONES GEOVICTORIA

geovictoria = pd.read_excel(
    "datos/geovictoria.xlsx",
    header=1
)

#print(geovictoria.columns.to_list())

columnas_geovictoria = [
    "Apellidos",
    "Nombre",
    "Identificador",
    "Fecha",
    "Entró",
    "Salió",
    "Entró.1",
    "Salió.1",
    
]

geovictoria = geovictoria[columnas_geovictoria]

geovictoria = geovictoria.rename(
    columns={
        "Entró": "hora_ingreso",
        "Salió": "inicio_colacion",
        "Entró.1": "fin_colacion",
        "Salió.1": "hora_salida"
    }
)

#print(geovictoria.head())
#print(geovictoria.columns.to_list())
#print(geovictoria["Fecha"].str.endswith("(F)").sum()) # Revision de feriados
fecha_limpia = geovictoria["Fecha"].str[-10:]
#print(fecha_limpia.head())

geovictoria["fecha"] = pd.to_datetime(fecha_limpia, format="%d-%m-%Y")
#print(geovictoria[["Fecha", "fecha"]].head())
#print(geovictoria["fecha"].dtype)

#print(geovictoria["Identificador"].head(5))
#print(ruta_maestro["rut"].head(5))

rut_geo_invalido = ~(geovictoria["Identificador"].isin(ruta_maestro["rut"]))
rut_geo_invalido.reset_index()
#print(geovictoria[rut_geo_invalido]["Identificador"].value_counts()) Para mirar dentro de la mascara rut_geo... columnas que existen en geovictoria

identificadores_excluidos = [
    "17.213.420-3"
]

es_id_excluido = geovictoria["Identificador"].isin(identificadores_excluidos)
#print(es_id_excluido.sum())

rut_geo_realmente_invalido = (es_id_excluido == False) & ~(geovictoria["Identificador"].isin(ruta_maestro["rut"]))
#print(rut_geo_realmente_invalido.sum())

geovictoria_laboral = geovictoria[
    ~es_id_excluido
].copy()

#print(len(geovictoria_laboral))
#print(len(geovictoria))

geovictoria_con_id = geovictoria_laboral.merge(ruta_maestro[["rut", "trabajador_id"]],
            left_on= "Identificador",
            right_on= "rut",
            how="left"

)
#print(geovictoria_con_id.columns.tolist())
##print(geovictoria_con_id[["Identificador", "rut", "trabajador_id"]].head(10))
#print(geovictoria_con_id["trabajador_id"].isna().sum())

#print(geovictoria_con_id["trabajador_id"].dtype)
#print(cronograma_mensual["trabajador_id"].dtype)

#print(geovictoria_con_id["fecha"].dtype)
#print(cronograma_mensual["fecha"].dtype)

marcaciones_duplicadas = geovictoria_con_id.duplicated(
    subset=["trabajador_id", "fecha"],
    keep=False
)
#print(marcaciones_duplicadas.sum())
cruce_asistencia = cronograma_mensual.merge(
    geovictoria_con_id, 
    on=["trabajador_id", "fecha"],
    how="outer",
    indicator=True
)

#print(cruce_asistencia["_merge"].value_counts())
solo_geovictoria = cruce_asistencia["_merge"] == "right_only"
#print(solo_geovictoria.sum())
fila_solo_geovictoria = cruce_asistencia[solo_geovictoria]
#print(fila_solo_geovictoria["fecha"])
fin_semana_sin_marcaciones = fila_solo_geovictoria[[
    "hora_ingreso",
    "inicio_colacion",
    "fin_colacion",
    "hora_salida"]
].isna().all(axis=1)


#print(fin_semana_sin_marcaciones.sum())

fin_semana_con_marcacion = ~fila_solo_geovictoria[[
    "hora_ingreso",
    "inicio_colacion",
    "fin_colacion",
    "hora_salida"]
].isna().all(axis=1)

#print(fin_semana_con_marcacion.sum())
fin_semana_con_marcaciones = fila_solo_geovictoria[fin_semana_con_marcacion]
"""print(fin_semana_con_marcaciones[[
    "Nombre",
    "Apellidos",
    "Fecha",
    "hora_ingreso",
    "inicio_colacion",
    "fin_colacion",
    "hora_salida"
    ]])"""
#print(geovictoria_con_id["fecha"].min())

fecha_inicio_periodo = geovictoria_con_id["fecha"].min()
#print(fecha_inicio_periodo)

posible_arrastre_periodo_anterior = ((fila_solo_geovictoria["fecha"] == fecha_inicio_periodo) 
                                    & (fila_solo_geovictoria["hora_ingreso"].isna())
                                    & (fila_solo_geovictoria["inicio_colacion"].isna())
                                    & (fila_solo_geovictoria["fin_colacion"].isna())
                                    & (fila_solo_geovictoria["hora_salida"].notna())
                )

#print(posible_arrastre_periodo_anterior.sum())

incidencias_geovictoria = fila_solo_geovictoria.copy()
incidencias_geovictoria["clasificacion"] = "REQUIERE_REVISION"
#print(incidencias_geovictoria["clasificacion"].value_counts())

incidencias_geovictoria.loc[fin_semana_sin_marcaciones, "clasificacion"]= "SIN_MARCACIONES"
#print(incidencias_geovictoria)

incidencias_geovictoria.loc[posible_arrastre_periodo_anterior, "clasificacion"] = "POSIBLE_ARRASTRE_PERIODO_ANTERIOR"
#print(incidencias_geovictoria["clasificacion"].value_counts())

coincide_cronograma_geovictoria = cruce_asistencia["_merge"] == "both"
jornadas_programadas = cruce_asistencia[coincide_cronograma_geovictoria].copy()
#print(len(jornadas_programadas))

marcacion_completa = jornadas_programadas[[
        "hora_ingreso",
        "inicio_colacion",
        "fin_colacion",
        "hora_salida"
    ]
].notna().all(axis=1)
#print(marcacion_completa.sum())
#print((~marcacion_completa).sum())

#print(jornadas_programadas["estado_programado"].value_counts())
es_jornada_trabajo = jornadas_programadas["estado_programado"] == "trabajo"
jornadas_trabajo = jornadas_programadas[es_jornada_trabajo].copy()
#print(len(jornadas_trabajo))

marcacion_completa_trabajo = jornadas_trabajo[[
        "hora_ingreso",
        "inicio_colacion",
        "fin_colacion",
        "hora_salida"
    ]
].notna().all(axis=1)

#print(marcacion_completa_trabajo.sum())
#print((~marcacion_completa_trabajo).sum())

cantidad_marcaciones_trabajo = jornadas_trabajo[[
        "hora_ingreso",
        "inicio_colacion",
        "fin_colacion",
        "hora_salida"

    ]
].notna().sum(axis=1)

#print(cantidad_marcaciones_trabajo.value_counts().sort_index())

jornadas_incompletas = jornadas_trabajo[~marcacion_completa_trabajo].copy()
#print(len(jornadas_incompletas))

"""print(jornadas_incompletas[[
        "hora_ingreso",
        "inicio_colacion",
        "fin_colacion",
        "hora_salida"
    ]
].isna().sum())"""

marcaciones_faltantes = jornadas_incompletas[[
    "hora_ingreso",
    "inicio_colacion",
    "fin_colacion",
    "hora_salida"
    ]
].isna()

#print(marcaciones_faltantes.value_counts())

#print(jornadas_incompletas.columns.tolist())

sin_marcaciones_colacion = (
    (jornadas_incompletas["hora_ingreso"].notna())
    &(jornadas_incompletas["inicio_colacion"].isna())
    &(jornadas_incompletas["fin_colacion"].isna())
    &(jornadas_incompletas["hora_salida"].notna())
)

#print(sin_marcaciones_colacion.sum())

jornadas_sin_marcaciones_colacion =jornadas_incompletas[sin_marcaciones_colacion].copy()
#print(len(jornadas_sin_marcaciones_colacion))

#print(jornadas_sin_marcaciones_colacion["colacion_programada_minutos"].value_counts(dropna=False))

colacion_programada_sin_marcaciones = (jornadas_sin_marcaciones_colacion["colacion_programada_minutos"] == 60)
#print(colacion_programada_sin_marcaciones.sum())
"""print(jornadas_sin_marcaciones_colacion.loc[colacion_programada_sin_marcaciones,
    [
    "nombre",
    "fecha",
    "entrada_programada",
    "salida_programada",
    "colacion_programada_minutos",
    "hora_ingreso",
    "inicio_colacion",
    "fin_colacion",
    "hora_salida"
]])

print(jornadas_sin_marcaciones_colacion.loc[colacion_programada_sin_marcaciones,
        [
        "nombre",
        "fecha",
        "observacion"
    ]
]
)"""

falta_inicio_colacion = (
    (jornadas_incompletas["hora_ingreso"].notna())
    &(jornadas_incompletas["inicio_colacion"].isna())
    &(jornadas_incompletas["fin_colacion"].notna())
    &(jornadas_incompletas["hora_salida"].notna())
)
#print(falta_inicio_colacion.sum())

jornadas_falta_inicio_colacion = jornadas_incompletas[falta_inicio_colacion].copy()
#print(jornadas_falta_inicio_colacion["colacion_programada_minutos"].value_counts(dropna=False))

jornadas_falta_inicio_colacion["inicio_colacion_ajustada"] = jornadas_falta_inicio_colacion["fin_colacion"]
"""print(jornadas_falta_inicio_colacion[[
    "nombre",
    "fin_colacion",
    "inicio_colacion_ajustada"

    ]])
"""
#print(jornadas_falta_inicio_colacion["colacion_programada_minutos"].dtype)
jornadas_falta_inicio_colacion["duracion_colacion_programada"] = pd.to_timedelta(jornadas_falta_inicio_colacion["colacion_programada_minutos"], unit="m")
"""print(  
    jornadas_falta_inicio_colacion[[
        "colacion_programada_minutos", "duracion_colacion_programada"
    ]]
)"""

jornadas_falta_inicio_colacion["inicio_colacion_ajustada"] = (jornadas_falta_inicio_colacion["fin_colacion"]- jornadas_falta_inicio_colacion["duracion_colacion_programada"])
"""print(jornadas_falta_inicio_colacion[[
    "nombre",
    "fin_colacion",
    "duracion_colacion_programada",
    "inicio_colacion_ajustada"
]])"""

inicio_colacion_ajustada_fuera_jornada = jornadas_falta_inicio_colacion["inicio_colacion_ajustada"] <= jornadas_falta_inicio_colacion["hora_ingreso"]

jornadas_falta_inicio_colacion["estado_ajuste"] = "AJUSTADO_AUTOMATICAMENTE"
jornadas_falta_inicio_colacion["motivo_ajuste"] = "FALTA_INICIO_COLACION"
jornadas_falta_inicio_colacion.loc[
    inicio_colacion_ajustada_fuera_jornada, "estado_ajuste"
] = "REQUIERE_REVISION"

jornadas_falta_inicio_colacion.loc[
    inicio_colacion_ajustada_fuera_jornada, "motivo_ajuste"
] = "INICIO_COLACION_AJUSTADO_FUERA_JORNADA"

#print(inicio_colacion_ajustada_fuera_jornada.sum())

"""print(jornadas_falta_inicio_colacion[[
    "nombre",
    "inicio_colacion",
    "inicio_colacion_ajustada",
    "estado_ajuste",
    "motivo_ajuste"

]])"""

falta_fin_colacion = (
    (jornadas_incompletas["hora_ingreso"].notna())
    & (jornadas_incompletas["inicio_colacion"].notna())
    & (jornadas_incompletas["fin_colacion"].isna())
    &(jornadas_incompletas["hora_salida"].notna())
)

jornadas_falta_fin_colacion = jornadas_incompletas[falta_fin_colacion].copy()
#print(len(jornadas_falta_fin_colacion))
#print(jornadas_falta_fin_colacion["colacion_programada_minutos"].value_counts(dropna=False))
jornadas_falta_fin_colacion["duracion_colacion_programada"] = pd.to_timedelta(jornadas_falta_fin_colacion["colacion_programada_minutos"], unit="m")
"""print(jornadas_falta_fin_colacion[[
        "duracion_colacion_programada",
        "colacion_programada_minutos"
]]
)"""
jornadas_falta_fin_colacion["fin_colacion_ajustada"] = jornadas_falta_fin_colacion["inicio_colacion"]+ jornadas_falta_fin_colacion["duracion_colacion_programada"]
fin_colacion_ajustada_fuera_jornada = jornadas_falta_fin_colacion["fin_colacion_ajustada"]>jornadas_falta_fin_colacion["hora_salida"]
jornadas_falta_fin_colacion["estado_ajuste"] = "AJUSTADO_AUTOMATICAMENTE"
jornadas_falta_fin_colacion["motivo_ajuste"] = "FALTA_FIN_COLACION"

jornadas_falta_fin_colacion.loc[
    fin_colacion_ajustada_fuera_jornada, "estado_ajuste"
] = "REQUIERE_REVISION"
jornadas_falta_fin_colacion.loc[
    fin_colacion_ajustada_fuera_jornada, "motivo_ajuste"
] = "FIN_COLACION_AJUSTADA_FUERA_JORNADA"

"""print(jornadas_falta_fin_colacion[[
    "nombre",
    "inicio_colacion",
    "fin_colacion",
    "duracion_colacion_programada",
    "fin_colacion_ajustada",
    "estado_ajuste",
    "motivo_ajuste"


]])"""

#print(fin_colacion_ajustada_fuera_jornada.sum())

falta_hora_ingreso = (
    (jornadas_incompletas["hora_ingreso"].isna())
    &(jornadas_incompletas["inicio_colacion"].notna())
    &(jornadas_incompletas["fin_colacion"].notna())
    &(jornadas_incompletas["hora_salida"].notna())
)

#print(falta_hora_ingreso.sum())

jornadas_falta_ingreso = jornadas_incompletas[falta_hora_ingreso].copy()
"""print(jornadas_falta_ingreso[[
    "nombre",
    "fecha",
    "entrada_programada",
    "salida_programada",
    "colacion_programada_minutos",
    "hora_ingreso",
    "inicio_colacion",
    "fin_colacion",
    "hora_salida",
    "observacion"
]])"""

#print(jornadas_falta_ingreso[["entrada_programada", "inicio_colacion"]].dtypes)
#print(type(jornadas_falta_ingreso["entrada_programada"].iloc[0]))

entrada_programada_timedelta = pd.to_timedelta(jornadas_falta_ingreso["entrada_programada"].astype(str))
#print(entrada_programada_timedelta)
#print(entrada_programada_timedelta.dtypes)

diferencia_primera_marca = (
    jornadas_falta_ingreso["inicio_colacion"] - entrada_programada_timedelta
)

jornadas_falta_ingreso["estado_ajuste"] = "REQUIERE_REVISION"
jornadas_falta_ingreso["motivo_ajuste"] = "FALTA_HORA_INGRESO"


#print(diferencia_primera_marca)
diferencia_primera_marca_minutos = (diferencia_primera_marca.dt.total_seconds()/60)
#print(diferencia_primera_marca_minutos)
falta_ingreso_marcaje_desplazado = (diferencia_primera_marca_minutos >= 0) & (diferencia_primera_marca_minutos <= 60 ) 
#print(falta_ingreso_marcaje_desplazado)
#print(falta_ingreso_marcaje_desplazado.sum())


jornadas_falta_ingreso.loc[
    falta_ingreso_marcaje_desplazado, "estado_ajuste"
] = "AJUSTADO_AUTOMATICAMENTE"
jornadas_falta_ingreso.loc[
    falta_ingreso_marcaje_desplazado, "motivo_ajuste"
] = "MARCAJE_DESPLAZADO"

"""print(jornadas_falta_ingreso[[
    "nombre",
    "estado_ajuste",
    "motivo_ajuste"
]]
)"""

jornadas_falta_ingreso["hora_ingreso_ajustada"] = jornadas_falta_ingreso["hora_ingreso"]
jornadas_falta_ingreso["inicio_colacion_ajustada"] = jornadas_falta_ingreso["inicio_colacion"]
jornadas_falta_ingreso["fin_colacion_ajustada"] = jornadas_falta_ingreso["fin_colacion"]

jornadas_falta_ingreso.loc[
    falta_ingreso_marcaje_desplazado, "hora_ingreso_ajustada"
] = jornadas_falta_ingreso.loc[
    falta_ingreso_marcaje_desplazado, "inicio_colacion"
]

"""print(jornadas_falta_ingreso[
    [
        "nombre",
        "hora_ingreso",
        "inicio_colacion",
        "hora_ingreso_ajustada"
        ]
    ]
)"""

jornadas_falta_ingreso.loc[
    falta_ingreso_marcaje_desplazado, "inicio_colacion_ajustada"
] = jornadas_falta_ingreso.loc[
    falta_ingreso_marcaje_desplazado, "fin_colacion"
]


jornadas_falta_ingreso["duracion_colacion_programada"] = pd.to_timedelta(jornadas_falta_ingreso["colacion_programada_minutos"], unit="m")
jornadas_falta_ingreso.loc[
    falta_ingreso_marcaje_desplazado, "fin_colacion_ajustada"
] = (jornadas_falta_ingreso["inicio_colacion_ajustada"]+ jornadas_falta_ingreso["duracion_colacion_programada"])

ajuste_desplazado_coherente = (jornadas_falta_ingreso["hora_ingreso_ajustada"] <= jornadas_falta_ingreso["inicio_colacion_ajustada"]) & (jornadas_falta_ingreso["inicio_colacion_ajustada"]<=jornadas_falta_ingreso["fin_colacion_ajustada"]) & (jornadas_falta_ingreso["fin_colacion_ajustada"] <= jornadas_falta_ingreso["hora_salida"])

#print(ajuste_desplazado_coherente)

"""print(jornadas_falta_ingreso[[
    "nombre",
    "hora_ingreso",
    "hora_ingreso_ajustada",
    "inicio_colacion",
    "inicio_colacion_ajustada",
    "fin_colacion",
    "fin_colacion_ajustada",
    "estado_ajuste",
    "motivo_ajuste"

]])"""

marcaje_desplazado_seguro = (falta_ingreso_marcaje_desplazado & ajuste_desplazado_coherente)
#print(marcaje_desplazado_seguro)
#print(marcaje_desplazado_seguro.sum())

jornadas_falta_ingreso["estado_ajuste"] = "REQUIERE_REVISION"
jornadas_falta_ingreso["motivo_ajuste"] = "FALTA_HORA_INGRESO"

jornadas_falta_ingreso.loc[
    marcaje_desplazado_seguro, "estado_ajuste"
] = "AJUSTADO_AUTOMATICAMENTE"

jornadas_falta_ingreso.loc[
    marcaje_desplazado_seguro, "motivo_ajuste"
] = "MARCAJE_DESPLAZADO"

"""print(jornadas_falta_ingreso[[
    "nombre",
    "hora_ingreso",
    "hora_ingreso_ajustada",
    "inicio_colacion",
    "inicio_colacion_ajustada",
    "fin_colacion",
    "fin_colacion_ajustada",
    "hora_salida",
    "estado_ajuste",
    "motivo_ajuste"

]])"""

falta_ingreso_y_fin_colacion =(
    (jornadas_incompletas["hora_ingreso"].isna()) 
    & (jornadas_incompletas["inicio_colacion"].notna())
    & (jornadas_incompletas["fin_colacion"].isna())
    & (jornadas_incompletas["hora_salida"].notna())
)

#print(falta_ingreso_y_fin_colacion.sum())

dt_falta_ingreso_fin_colacion = jornadas_incompletas[falta_ingreso_y_fin_colacion].copy()

dt_falta_ingreso_fin_colacion["estado_ajuste"] = "REQUIERE_REVISION"
dt_falta_ingreso_fin_colacion["motivo_ajuste"] = "FALTA_INGRESO_Y_FIN_COLACION"

entrada_programada_timedelta2 = pd.to_timedelta(dt_falta_ingreso_fin_colacion["entrada_programada"].astype(str))
diferencia_primera_marca_minutos_2 =((dt_falta_ingreso_fin_colacion["inicio_colacion"] - entrada_programada_timedelta2).dt.total_seconds())/60
#print(diferencia_primera_marca_minutos_2)
marcaje_desplazado_sin_colacion = (diferencia_primera_marca_minutos_2 >= 0) & (diferencia_primera_marca_minutos_2 <= 60)
#print(marcaje_desplazado_sin_colacion)

#print(dt_falta_ingreso_fin_colacion.columns.to_list())

dt_falta_ingreso_fin_colacion["hora_ingreso_ajustada"] = dt_falta_ingreso_fin_colacion["hora_ingreso"]

dt_falta_ingreso_fin_colacion.loc[
    marcaje_desplazado_sin_colacion, "hora_ingreso_ajustada"
] = dt_falta_ingreso_fin_colacion.loc[
    marcaje_desplazado_sin_colacion, "inicio_colacion"
]

dt_falta_ingreso_fin_colacion.loc[
    marcaje_desplazado_sin_colacion, "estado_ajuste"
] = "AJUSTADO_AUTOMATICAMENTE"
dt_falta_ingreso_fin_colacion.loc[
    marcaje_desplazado_sin_colacion, "motivo_ajuste"
] = "MARCAJE_DESPLAZADO_SIN_COLACION"
"""
print(dt_falta_ingreso_fin_colacion[[
    "nombre",
    "fecha",
    "entrada_programada",
    "salida_programada",
    "hora_ingreso",
    "hora_ingreso_ajustada",
    "inicio_colacion",
    "fin_colacion",
    "hora_salida",
    "estado_ajuste",
    "motivo_ajuste"
]])"""

sin_marcaciones_trabajo = (cantidad_marcaciones_trabajo == 0)
#print(sin_marcaciones_trabajo.sum())


dt_sin_marcaciones_jornada_trabajo = jornadas_trabajo[sin_marcaciones_trabajo].copy()

dt_sin_marcaciones_jornada_trabajo["estado_asistencia"] = "REQUIERE_REVISION"

dt_sin_marcaciones_jornada_trabajo["motivo_asistencia"] = "SIN_MARCACIONES"


"""print(dt_sin_marcaciones_jornada_trabajo[[
    "nombre",
    "fecha",
    "entrada_programada",
    "salida_programada",
    "colacion_programada_minutos",
    "hora_ingreso",
    "inicio_colacion",
    "fin_colacion",
    "hora_salida",
    "observacion" 
]])"""

es_permiso_medico = (dt_sin_marcaciones_jornada_trabajo["observacion"].str.contains("permiso medico", case=False, na=False))
dt_sin_marcaciones_jornada_trabajo.loc[
    es_permiso_medico, "estado_asistencia"
] = "AUSENCIA_JUSTIFICADA"
dt_sin_marcaciones_jornada_trabajo.loc[
    es_permiso_medico, "motivo_asistencia"
] = "PERMISO_MEDICO"

"""print(dt_sin_marcaciones_jornada_trabajo[[
    "nombre",
    "fecha",
    "estado_asistencia",
    "motivo_asistencia"
]])"""
#print(es_permiso_medico.sum())
es_dia_libre = (jornadas_programadas["estado_programado"] == "libre")
#print(es_dia_libre.sum())

jornadas_libres = jornadas_programadas[es_dia_libre].copy()
jornadas_libres["estado_asistencia"] = "REQUIERE_REVISION"
jornadas_libres["motivo_asistencia"] = "MARCACION_O_SITUACION_EN_DIA_LIBRE"

#print(len(jornadas_libres))
"""print(jornadas_libres[[
    "nombre",
    "fecha",
    "observacion"
]])"""

cantidad_marcaciones_libres = (
    jornadas_libres[["hora_ingreso", "inicio_colacion", "fin_colacion", "hora_salida"]].notna().sum(axis=1)
)
#print(cantidad_marcaciones_libres.value_counts().sort_index())
es_vacaciones = (jornadas_libres["observacion"].str.contains("vacaciones", case=False, na=False))
#print(es_vacaciones.sum())

vacaciones_sin_marcaciones = (
    es_vacaciones & (cantidad_marcaciones_libres == 0)
)

jornadas_libres.loc[
    vacaciones_sin_marcaciones, "estado_asistencia"] = "AUSENCIA_JUSTIFICADA"
jornadas_libres.loc[
    vacaciones_sin_marcaciones, "motivo_asistencia"] = "VACACIONES"
"""
print(jornadas_libres[[
    "nombre",
    "fecha",
    "observacion",
    "estado_asistencia",
    "motivo_asistencia"
]])
"""

total_patrones_incompletos = (
    falta_inicio_colacion.sum()
    + falta_fin_colacion.sum()
    + sin_marcaciones_colacion.sum()
    + falta_hora_ingreso.sum()
    + falta_ingreso_y_fin_colacion.sum()
    + sin_marcaciones_trabajo.sum()
)

#print(total_patrones_incompletos)
#print(len(jornadas_incompletas))
cobertura_patrones = pd.DataFrame({
    "falta_inicio_colacion": falta_inicio_colacion,
    "falta_fin_colacion": falta_fin_colacion,
    "sin_marcaciones_colacion": sin_marcaciones_colacion,
    "falta_hora_ingreso": falta_hora_ingreso,
    "falta_ingreso_y_fin_colacion": falta_ingreso_y_fin_colacion,
    "sin_marcaciones_jornada_trabajo": sin_marcaciones_trabajo
})

cantidad_patrones_por_fila = cobertura_patrones.sum(axis=1)
#print(cantidad_patrones_por_fila.value_counts().sort_index())

total_ajustadas_automaticamente = (
    falta_inicio_colacion.sum()
    + falta_fin_colacion.sum()
    + marcaje_desplazado_seguro.sum()
    + marcaje_desplazado_sin_colacion.sum()
)
#print(total_ajustadas_automaticamente)

sin_colacion_no_programada = (sin_marcaciones_colacion) & (jornadas_incompletas["colacion_programada_minutos"]== 0)
total_sin_ajuste = sin_colacion_no_programada.sum()
#print(total_sin_ajuste)

#print(es_permiso_medico.sum())

#print(colacion_programada_sin_marcaciones.sum())
#print((jornadas_falta_ingreso["estado_ajuste"] == "REQUIERE_REVISION").sum())
#print((dt_falta_ingreso_fin_colacion["estado_ajuste"] == "REQUIERE_REVISION").sum())
"""
print(
    jornadas_sin_marcaciones_colacion.loc[
        colacion_programada_sin_marcaciones,
        [
            "nombre",
            "fecha",
            "estado_programado",
            "colacion_programada_minutos",
            "hora_ingreso",
            "inicio_colacion",
            "fin_colacion",
            "hora_salida"
        ]
    ]
)

print(
    jornadas_falta_ingreso.loc[
        jornadas_falta_ingreso["estado_ajuste"] == "REQUIERE_REVISION",
        [
            "nombre",
            "fecha",
            "entrada_programada",
            "hora_ingreso",
            "inicio_colacion",
            "fin_colacion",
            "hora_salida",
            "motivo_ajuste"
        ]
    ]
)

print(
    dt_falta_ingreso_fin_colacion.loc[
        dt_falta_ingreso_fin_colacion["estado_ajuste"] == "REQUIERE_REVISION",
        [
            "nombre",
            "fecha",
            "entrada_programada",
            "hora_ingreso",
            "inicio_colacion",
            "fin_colacion",
            "hora_salida",
            "motivo_ajuste"
        ]
    ]
)"""

jornadas_clasificadas = jornadas_incompletas.copy()

jornadas_clasificadas["estado_asistencia"] = "REQUIERE_REVISION"
jornadas_clasificadas["motivo_asistencia"] = "PATRON_NO_RESUELTO"

#print(jornadas_clasificadas["estado_asistencia"].value_counts())

jornadas_clasificadas.loc[
    sin_colacion_no_programada, "estado_asistencia"
] = "OK"

jornadas_clasificadas.loc[
    sin_colacion_no_programada, "motivo_asistencia"
] = "SIN_COLACION_PROGRAMADA"

#print(jornadas_clasificadas["estado_asistencia"].value_counts())

indices_falta_inicio_auto = jornadas_falta_inicio_colacion.index[
    jornadas_falta_inicio_colacion["estado_ajuste"] == "AJUSTADO_AUTOMATICAMENTE"
]

#print(indices_falta_inicio_auto)
#print(len(indices_falta_inicio_auto))

jornadas_clasificadas.loc[
    indices_falta_inicio_auto, "estado_asistencia"
] = "AJUSTADO_AUTOMATICAMENTE"

jornadas_clasificadas.loc[
    indices_falta_inicio_auto, "motivo_asistencia"
] = "FALTA_INICIO_COLACION"

#print(jornadas_clasificadas["estado_asistencia"].value_counts())

jornadas_clasificadas["inicio_colacion_ajustada"] = (jornadas_clasificadas["inicio_colacion"])

jornadas_clasificadas.loc[
    indices_falta_inicio_auto, "inicio_colacion_ajustada"
] = jornadas_falta_inicio_colacion.loc[
    indices_falta_inicio_auto, "inicio_colacion_ajustada"
]

"""print(jornadas_clasificadas.loc[
        indices_falta_inicio_auto,
        [   
            "nombre",
            "fecha",
            "inicio_colacion",
            "inicio_colacion_ajustada",
            "estado_asistencia",
            "motivo_asistencia"
        ]
])"""

indices_falta_fin_auto = jornadas_falta_fin_colacion.index[
    jornadas_falta_fin_colacion["estado_ajuste"] == "AJUSTADO_AUTOMATICAMENTE"
]

#print(len(indices_falta_fin_auto))
jornadas_clasificadas.loc[
    indices_falta_fin_auto,
    "estado_asistencia"
] = "AJUSTADO_AUTOMATICAMENTE"

jornadas_clasificadas.loc[
    indices_falta_fin_auto, "motivo_asistencia"
] = "FALTA_FIN_COLACION"

jornadas_clasificadas["fin_colacion_ajustada"] = (
    jornadas_clasificadas["fin_colacion"]
)

jornadas_clasificadas.loc[
    indices_falta_fin_auto,
    "fin_colacion_ajustada"
] = jornadas_falta_fin_colacion.loc[
    indices_falta_fin_auto,
    "fin_colacion_ajustada"
]

#print(jornadas_clasificadas["estado_asistencia"].value_counts())

jornadas_clasificadas["hora_ingreso_ajustada"] = (
    jornadas_clasificadas["hora_ingreso"]
)
indices_marcaje_desplazado = jornadas_falta_ingreso.index[
    jornadas_falta_ingreso["estado_ajuste"] == "AJUSTADO_AUTOMATICAMENTE"
]

#print(len(indices_marcaje_desplazado))

jornadas_clasificadas.loc[
    indices_marcaje_desplazado,
    "estado_asistencia"
] = "AJUSTADO_AUTOMATICAMENTE"

jornadas_clasificadas.loc[
    indices_marcaje_desplazado,
    "motivo_asistencia"
] = "MARCAJE_DESPLAZADO"

jornadas_clasificadas.loc[
    indices_marcaje_desplazado, "hora_ingreso_ajustada"
] = jornadas_falta_ingreso.loc[indices_marcaje_desplazado, "hora_ingreso_ajustada"]

indice_desplazado_sin_colacion = dt_falta_ingreso_fin_colacion.index[
    dt_falta_ingreso_fin_colacion["estado_ajuste"] == "AJUSTADO_AUTOMATICAMENTE"
]

jornadas_clasificadas.loc[
    indice_desplazado_sin_colacion, "estado_asistencia"

] = "AJUSTADO_AUTOMATICAMENTE"
jornadas_clasificadas.loc[
    indice_desplazado_sin_colacion, "motivo_asistencia"
] = "MARCAJE_DESPLAZADO_SIN_COLACION"

jornadas_clasificadas.loc[
    indice_desplazado_sin_colacion, "hora_ingreso_ajustada"
] = dt_falta_ingreso_fin_colacion.loc[
    indice_desplazado_sin_colacion, "hora_ingreso_ajustada"
]

#print(jornadas_clasificadas["estado_asistencia"].value_counts())

#print(jornadas_clasificadas["estado_asistencia"].value_counts())
#print(indices_marcaje_desplazado)
#print(indice_desplazado_sin_colacion)
"""
print(
    jornadas_clasificadas.loc[
        list(indices_marcaje_desplazado) + list(indice_desplazado_sin_colacion),
        [
            "nombre",
            "fecha",
            "estado_asistencia",
            "motivo_asistencia",
            "hora_ingreso",
            "hora_ingreso_ajustada"

        ]
    ]
)"""

indices_permiso_medico = dt_sin_marcaciones_jornada_trabajo.index[
    dt_sin_marcaciones_jornada_trabajo["estado_asistencia"] == "AUSENCIA_JUSTIFICADA"
]
#print(indices_permiso_medico)
#print(len(indices_permiso_medico))

jornadas_clasificadas.loc[
    indices_permiso_medico,
    "estado_asistencia"
] = "AUSENCIA_JUSTIFICADA"

jornadas_clasificadas.loc[
    indices_permiso_medico,
    "motivo_asistencia"
] = "PERMISO_MEDICO"

#rint(jornadas_clasificadas["estado_asistencia"].value_counts())
#print(jornadas_clasificadas["motivo_asistencia"].value_counts())

indices_colacion_revision = jornadas_sin_marcaciones_colacion.index[
    colacion_programada_sin_marcaciones
]

print(indices_colacion_revision)
jornadas_clasificadas.loc[
    indices_colacion_revision
]

jornadas_clasificadas.loc[
    indices_colacion_revision,
    "motivo_asistencia"
] = "COLACION_PROGRAMADA_SIN_MARCACIONES"

indices_falta_ingreso_revision = jornadas_falta_ingreso.index[
    jornadas_falta_ingreso["estado_ajuste"] == "REQUIERE_REVISION"]

jornadas_clasificadas.loc[
    indices_falta_ingreso_revision,
    "motivo_asistencia"
] = "FALTA_HORA_INGRESO"

indices_falta_ingreso_fin_revision = dt_falta_ingreso_fin_colacion.index[
    dt_falta_ingreso_fin_colacion["estado_ajuste"] == "REQUIERE_REVISION"
]

jornadas_clasificadas.loc[
    indices_falta_ingreso_fin_revision,
    "motivo_asistencia"
] = "FALTA_INGRESO_Y_FIN_COLACION"

"""print(jornadas_clasificadas.loc[
    jornadas_clasificadas["motivo_asistencia"] == "PATRON_NO_RESUELTO",
    [
        "nombre",
        "fecha",
        "estado_asistencia",
        "motivo_asistencia",
        "hora_ingreso",
        "inicio_colacion",
        "fin_colacion",
        "hora_salida"
    ]
]
)"""

print(jornadas_clasificadas["motivo_asistencia"].value_counts())