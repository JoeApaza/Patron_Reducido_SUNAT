# main.py

import zipfile
import logging

from descargar_zip import obtener_contenido_pagina, extraer_fecha_y_enlace, descargar_archivo
from procesar_zip import (
    abrir_archivo_zip,
    contar_filas_archivo,
    leer_y_procesar_chunks,
    manejar_columna_extra,
    guardar_muestra_excel,
    print_tiempo_inicio,
    print_tiempo_fin
)

# Configuración del registro (logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        # Sobrescribe el archivo 'app.log' y lo codifica en UTF-8
        logging.FileHandler('app.log', mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    # URL de la página que contiene el enlace de descarga
    url_pagina = "https://www.sunat.gob.pe/descargaPRR/mrc137_padron_reducido.html"

    # Paso 1: Obtener el contenido de la página
    html_content = obtener_contenido_pagina(url_pagina)
    if not html_content:
        logger.error("No se pudo obtener el contenido de la página.")
        return

    # Paso 2: Extraer la fecha de actualización y el enlace de descarga
    fecha_actualizacion, url_descarga = extraer_fecha_y_enlace(html_content)
    if not url_descarga:
        logger.error("No se pudo obtener el enlace de descarga.")
        return

    # Paso 3: Descargar el archivo ZIP
    nombre_archivo_zip = "padron_reducido_ruc.zip"
    if not descargar_archivo(url_descarga, nombre_archivo_zip):
        logger.error("No se pudo descargar el archivo.")
        return

    # Paso 4: Procesar el archivo ZIP y cargar el DataFrame
    # Medición del tiempo total del script
    inicio_total = print_tiempo_inicio("Proceso completo")

    # Columnas esperadas
    columnas_esperadas = 15

    # 1. Abrir el archivo ZIP
    nombre_archivo = abrir_archivo_zip(nombre_archivo_zip)

    with zipfile.ZipFile(nombre_archivo_zip, 'r') as zip_ref:
        with zip_ref.open(nombre_archivo) as archivo_zip:
            # 2. Contar el número total de filas en el archivo
            total_filas_archivo = contar_filas_archivo(archivo_zip)

            # 3. Leer el archivo y procesar en chunks
            df, total_filas_dataframe, nombres_columnas, bad_lines = leer_y_procesar_chunks(archivo_zip, columnas_esperadas)

    # 4. Manejar la columna 'Extra' si existe
    df = manejar_columna_extra(df, columnas_esperadas, nombres_columnas)

    # 5. Mostrar el total de filas
    total_filas_archivo_datos = total_filas_archivo - 1  # Restamos 1 por la fila de encabezados
    logger.info(f"Total de filas en el archivo (datos): {total_filas_archivo_datos}")
    logger.info(f"Total de filas en el DataFrame: {total_filas_dataframe}")

    # 6. Comparar los totales de filas
    if total_filas_archivo_datos == total_filas_dataframe:
        logger.info("El número de filas en el archivo y en el DataFrame es el mismo.")
    else:
        diferencia = total_filas_archivo_datos - total_filas_dataframe
        logger.warning(f"Hay una diferencia de {diferencia} filas entre el archivo y el DataFrame.")
        logger.warning(f"Total de líneas problemáticas capturadas: {len(bad_lines)}")
        if bad_lines:
            logger.debug("Ejemplos de líneas problemáticas:")
            for i, line in enumerate(bad_lines[:5], 1):
                logger.debug(f"Línea {i}: {line}")

    # 7. Guardar una muestra de datos en un archivo Excel
    #guardar_muestra_excel(df)

    # Fin del proceso completo
    fin_total = print_tiempo_fin("Proceso completo", inicio_total)

if __name__ == "__main__":
    main()
