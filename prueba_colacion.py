from datetime import datetime


def calcular_duracion_colacion (hora_inicio, hora_fin):
    hora_inicio = datetime.strptime(hora_inicio, "%H%M")
    hora_fin = datetime.strptime(hora_fin, "%H%M")
    duracion_colacion = hora_fin - hora_inicio
    segundos_colacion = duracion_colacion.total_seconds()
    minutos_colacion = segundos_colacion / 60
    return int(minutos_colacion)



def calcular_colacion (colacion):
    if colacion > 60:
        return colacion
    elif colacion >= 35:
        return 60
    else:
        return 30
    
duracion_real = calcular_duracion_colacion("1300", "1325")
duracion_ajustada = calcular_colacion(duracion_real)
print(duracion_ajustada)
duracion_real = calcular_duracion_colacion("1300", "1335")
duracion_ajustada = calcular_colacion(duracion_real)
print(duracion_ajustada)
duracion_real = calcular_duracion_colacion("1300", "1400")
duracion_ajustada = calcular_colacion(duracion_real)
print(duracion_ajustada)
duracion_real = calcular_duracion_colacion("1300", "1415")
duracion_ajustada = calcular_colacion(duracion_real)
print(duracion_ajustada)


