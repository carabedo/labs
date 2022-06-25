import sys,csv, time
from datetime import datetime

# Constantes
POSICION_ARGUMENTO_NOMBRE_ARCHIVO   = 1
POSICION_ARGUMENTO_DNI              = 2
POSICION_ARGUMENTO_SALIDA           = 3
POSICION_ARGUMENTO_TIPO             = 4
POSICION_ARGUMENTO_OPTIONAL_1       = 5
POSICION_ARGUMENTO_OPTIONAL_2       = 6

ETIQUETA_CABECERA_CSV_DNI           = "DNI"
ETIQUETA_CABECERA_CSV_NUM_CHEQUE    = "NroCheque"
ETIQUETA_CABECERA_CSV_FECHA_ORIGEN  = "FechaOrigen"
ETIQUETA_CABECERA_CSV_FECHA_PAGO    = "FechaPago"
ETIQUETA_CABECERA_CSV_CUENTA_ORIGEN = "NumeroCuentaOrigen"
ETIQUETA_CABECERA_CSV_VALOR         = "Valor"
ETIQUETA_CABECERA_CSV_TIPO          = "Tipo"
ETIQUETA_CABECERA_CSV_ESTADO        = "Estado"

ESTADO_CHEQUE_APROBADO   = "APROBADO"
ESTADO_CHEQUE_PENDIENTE  = "PENDIENTE"
ESTADO_CHEQUE_RECHAZADO  = "RECHAZADO"

TIPO_SALIDA_PANTALLA = "PANTALLA"
TIPO_SALIDA_CSV      = "CSV"

RANGO_FECHA_INICIO  = 0
RANGO_FECHA_FIN     = 1

CANTIDAD_CON_UN_ATRIBUTOS_OPCIONALES  = 6
CANTIDAD_CON_DOS_ATRIBUTOS_OPCIONALES = 7

# El validar que es main es totalmente opcional a esta altura del programa.
if __name__ == '__main__':    
    # Puede usar with o bien abrir y cerrar el archivo.
    # Tambien puede recorrer linea por linea en lugar de leer de una.
    with open(sys.argv[POSICION_ARGUMENTO_NOMBRE_ARCHIVO]) as archivo:
        lector = csv.reader(archivo)
        datos = list(lector)
    
    cabecera = datos[0]
    
    # Tener presente que si no es encuentran las cabeceras, en el ejemplo salta excepcion
    (posicion_dni,
     posicion_numero_cheque,
     posicion_tipo_cheque,
     posicion_fecha_origen,
     posicion_fecha_pago,
     posicion_estado) =  (
                    cabecera.index(ETIQUETA_CABECERA_CSV_DNI),
                    cabecera.index(ETIQUETA_CABECERA_CSV_NUM_CHEQUE),
                    cabecera.index(ETIQUETA_CABECERA_CSV_TIPO), 
                    cabecera.index(ETIQUETA_CABECERA_CSV_FECHA_ORIGEN),
                    cabecera.index(ETIQUETA_CABECERA_CSV_FECHA_PAGO),
                    cabecera.index(ETIQUETA_CABECERA_CSV_ESTADO)
                    )
     
    # Se tratan los argumentos opcionales
    estado  = None
    fecha   = None
    
    # El orden es el establecido en el ejercicio, primero estado y luego fecha para facilidad
    if len(sys.argv) == CANTIDAD_CON_DOS_ATRIBUTOS_OPCIONALES:
        estado = sys.argv[POSICION_ARGUMENTO_OPTIONAL_1]
        fecha = tuple(map(lambda f: datetime.timestamp(datetime.strptime(f,'%d-%m-%Y')), sys.argv[POSICION_ARGUMENTO_OPTIONAL_2].split(":")))
    elif len(sys.argv) == CANTIDAD_CON_UN_ATRIBUTOS_OPCIONALES:
        if sys.argv[POSICION_ARGUMENTO_OPTIONAL_1] in [ESTADO_CHEQUE_APROBADO,ESTADO_CHEQUE_RECHAZADO,ESTADO_CHEQUE_PENDIENTE]:
            estado = sys.argv[POSICION_ARGUMENTO_OPTIONAL_1]
        else:
            fecha = tuple(map(lambda f: datetime.timestamp(datetime.strptime(f,'%d-%m-%Y')), sys.argv[POSICION_ARGUMENTO_OPTIONAL_1].split(":")))
            
    # Seguramente la siguiente linea cambie por un for y tambien busquen otra forma de remover la linea de header
    datos_cliente = list(filter(
        lambda registro: 
            registro[posicion_dni] == sys.argv[POSICION_ARGUMENTO_DNI] and 
            registro[posicion_tipo_cheque]==sys.argv[POSICION_ARGUMENTO_TIPO],
            datos[1:]))
    
    # Comprobamos si hay números de cheques repetidos
    listado_numero_cheques = list(map(lambda registro : registro[posicion_numero_cheque],datos_cliente))
    
    if len(listado_numero_cheques) != len(set(listado_numero_cheques)):
        print("Hay números de cheques repetidos en el archivo dado")
        sys.exit()    
        
    # Se filtra por estado de ser necesario
    if estado is not None:
        datos_cliente = list(filter(
                    lambda registro : 
                        registro[posicion_estado]==estado, 
                        datos_cliente))
    
    # Se filtra por fecha    
    if fecha is not None:
        datos_cliente = list(filter(
                    lambda registro : 
                        float(registro[posicion_fecha_origen]) > fecha[RANGO_FECHA_INICIO] and 
                        float(registro[posicion_fecha_origen]) < fecha[RANGO_FECHA_FIN], datos_cliente))
    
    salida = sys.argv[POSICION_ARGUMENTO_SALIDA]
    if  salida == TIPO_SALIDA_PANTALLA:
        print(",".join(cabecera)) 
        for t in datos_cliente:
            print(",".join(t))   
    elif salida == TIPO_SALIDA_CSV:
        posicion_cuenta_origen = cabecera.index(ETIQUETA_CABECERA_CSV_CUENTA_ORIGEN)
        posicion_valor = cabecera.index(ETIQUETA_CABECERA_CSV_VALOR)
        
        with open("{}_{}.csv".format(sys.argv[POSICION_ARGUMENTO_DNI],time.time()),"w") as f:
            writer = csv.writer(f)
            writer.writerow([cabecera[posicion_fecha_origen],cabecera[posicion_fecha_pago],cabecera[posicion_cuenta_origen],cabecera[posicion_valor],cabecera[posicion_estado]])
            for t in datos_cliente:
                writer.writerow([t[posicion_fecha_origen],t[posicion_fecha_pago],t[posicion_cuenta_origen],t[posicion_valor],t[posicion_estado]])
            print("CSV creado")
    else:
        print("Error con parámetro salida, debe ser del tipo {} o {}".format(TIPO_SALIDA_PANTALLA,TIPO_SALIDA_CSV))

    
    
    

