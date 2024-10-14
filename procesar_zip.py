# procesar_zip.py

import zipfile
import pandas as pd
import time
import csv
import logging

logger = logging.getLogger(__name__)

# Funciones para medir el tiempo de ejecución
def print_tiempo_inicio(nombre_proceso):
    inicio = time.time()
    logger.info(f"Iniciando {nombre_proceso}...")
    return inicio

def print_tiempo_fin(nombre_proceso, inicio):
    fin = time.time()
    duracion = fin - inicio
    logger.info(f"{nombre_proceso} finalizado. Tiempo tomado: {duracion:.2f} segundos.")
    return fin

# Función para abrir el archivo ZIP y obtener el archivo de datos
def abrir_archivo_zip(ruta_zip):
    inicio_proceso = print_tiempo_inicio("Abrir el archivo ZIP")
    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        contenido_zip = zip_ref.namelist()
        logger.info(f"Contenido del ZIP: {contenido_zip}")
        nombre_archivo = contenido_zip[0]
    fin_proceso = print_tiempo_fin("Abrir el archivo ZIP", inicio_proceso)
    return nombre_archivo

# Función para contar el número total de filas en el archivo
def contar_filas_archivo(archivo_zip):
    inicio_proceso = print_tiempo_inicio("Contar el número total de filas en el archivo")
    total_filas_archivo = sum(1 for _ in archivo_zip)
    archivo_zip.seek(0)
    logger.info(f"Total de filas en el archivo (incluyendo encabezados): {total_filas_archivo}")
    fin_proceso = print_tiempo_fin("Contar el número total de filas en el archivo", inicio_proceso)
    return total_filas_archivo

# Función para leer y procesar el archivo en chunks
def leer_y_procesar_chunks(archivo_zip, columnas_esperadas):
    inicio_proceso = print_tiempo_inicio("Leer el archivo y procesar en chunks")
    columns_to_read = list(range(columnas_esperadas + 1))  # Índices de columnas a leer
    lista_chunks = []
    total_filas_dataframe = 0
    nombres_columnas = None  # Se obtendrá de los encabezados del archivo
    bad_lines = []

    # Función para manejar las líneas con errores dentro del scope
    def bad_line_handler(line):
        bad_lines.append(line)
        logger.warning(f"Línea problemática omitida: {line}")
        return None  # Omitir la línea en el DataFrame

    # Leer el archivo en chunks usando el motor Python
    reader = pd.read_csv(
        archivo_zip,
        sep='|',
        engine='python',
        encoding='ISO-8859-1',
        dtype=str,
        na_filter=False,
        keep_default_na=False,
        chunksize=500000,
        quoting=csv.QUOTE_NONE,
        escapechar='\\',
        on_bad_lines=bad_line_handler,
        header=0,
        usecols=columns_to_read
    )

    for chunk_num, chunk in enumerate(reader):
        inicio_chunk = time.time()

        if chunk_num == 0:
            # Guardamos los nombres de las columnas
            nombres_columnas = chunk.columns.tolist()
            logger.info(f"Nombres de columnas obtenidos: {nombres_columnas}")
        else:
            # Asignamos los nombres de las columnas al chunk actual
            chunk.columns = nombres_columnas

        filas_chunk = chunk.shape[0]
        total_filas_dataframe += filas_chunk
        lista_chunks.append(chunk)

        fin_chunk = time.time()
        duracion_chunk = fin_chunk - inicio_chunk
        logger.info(f"Chunk {chunk_num + 1} procesado: {filas_chunk} filas en {duracion_chunk:.2f} segundos.")

    # Concatenar todos los chunks en un solo DataFrame
    df = pd.concat(lista_chunks, ignore_index=True)
    fin_proceso = print_tiempo_fin("Leer el archivo y procesar en chunks", inicio_proceso)
    return df, total_filas_dataframe, nombres_columnas, bad_lines

# Función para identificar y manejar la columna 'Extra' si existe
def manejar_columna_extra(df, columnas_esperadas, nombres_columnas):
    if len(df.columns) > columnas_esperadas:
        nombres_columnas = nombres_columnas[:columnas_esperadas] + ['Extra']
        df.columns = nombres_columnas

        filas_con_extra = df[df['Extra'].notna() & df['Extra'].str.strip().astype(bool)]

        if not filas_con_extra.empty:
            logger.warning(f"Se encontraron {len(filas_con_extra)} filas con valores en la columna 'Extra'.")
            logger.debug(f"Filas con valores en 'Extra':\n{filas_con_extra[['RUC', 'Extra']]}")
        else:
            logger.info("No se encontraron filas con valores en la columna 'Extra'.")

        # Decidir si eliminar la columna 'Extra'
        df = df.drop(columns=['Extra'])
    else:
        logger.info("No existe una columna 'Extra' en el DataFrame.")
    return df

# Función para guardar una muestra de datos en un archivo Excel
def guardar_muestra_excel(df, num_filas=100, nombre_archivo='muestra_datos.xlsx'):
    inicio_proceso = print_tiempo_inicio(f"Guardar las primeras {num_filas} filas en '{nombre_archivo}'")
    df_muestra = df.head(num_filas)
    df_muestra.to_excel(nombre_archivo, index=False)
    logger.info(f"Muestra guardada en '{nombre_archivo}'.")
    fin_proceso = print_tiempo_fin(f"Guardar las primeras {num_filas} filas en '{nombre_archivo}'", inicio_proceso)
