import pandas as pd #Llamo al directorio pandas y lo abrevio como pd
import openpyxl # Llamo al directorio openpyxl


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

