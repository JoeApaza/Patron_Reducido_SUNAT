# descargar_zip.py

import requests
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)

def obtener_contenido_pagina(url):
    """Accede a la página web y obtiene su contenido HTML."""
    try:
        logger.info(f"Accediendo a la página: {url}")
        response = requests.get(url)
        response.raise_for_status()
        logger.info("Contenido de la página obtenido correctamente.")
        return response.content
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al acceder a la página: {e}")
        return None

def extraer_fecha_y_enlace(html_content):
    """Extrae la fecha de actualización y el enlace de descarga del contenido HTML."""
    try:
        logger.info("Analizando el contenido de la página.")
        soup = BeautifulSoup(html_content, "html.parser")

        # Buscar la fecha de actualización dentro del elemento con clase 'titulo'
        titulo_element = soup.find("div", class_="titulo")
        fecha_actualizacion = None
        if titulo_element:
            texto_titulo = titulo_element.get_text(strip=True)
            # Extraer la fecha con una expresión regular que busca en formato dd/mm/yyyy
            fecha_actualizacion_match = re.search(r"\d{2}/\d{2}/\d{4}", texto_titulo)
            if fecha_actualizacion_match:
                fecha_actualizacion = fecha_actualizacion_match.group(0)
                logger.info(f"Fecha de actualización del padrón reducido: {fecha_actualizacion}")
            else:
                logger.warning("No se encontró la fecha en el formato dd/mm/yyyy.")
        else:
            logger.warning("No se encontró la fecha de actualización en la página.")

        # Buscar el enlace de descarga
        enlace_descarga = soup.find("a", href=True, string="padrón_reducido_RUC.zip")
        url_descarga = None
        if enlace_descarga:
            # Extraer la URL del archivo
            url_descarga = enlace_descarga['href']
            logger.info(f"Enlace de descarga encontrado: {url_descarga}")
        else:
            logger.error("Enlace de descarga no encontrado en la página.")

        return fecha_actualizacion, url_descarga
    except Exception as e:
        logger.error(f"Error al analizar el contenido de la página: {e}")
        return None, None


def descargar_archivo(url_descarga, nombre_archivo):
    """Descarga el archivo desde la URL proporcionada y lo guarda con el nombre especificado.
    
    Registra el progreso de la descarga cada 10%.
    """
    try:
        logger.info("Iniciando la descarga del archivo.")
        with requests.get(url_descarga, stream=True) as descarga_response:
            descarga_response.raise_for_status()
            # Obtener el tamaño total del archivo (si está disponible)
            total_tamano = int(descarga_response.headers.get('content-length', 0))
            chunk_size = 1024  # Tamaño de cada chunk en bytes
            tamano_descargado = 0
            last_logged_percentage = 0  # Último porcentaje registrado

            with open(nombre_archivo, "wb") as archivo:
                for chunk in descarga_response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        archivo.write(chunk)
                        tamano_descargado += len(chunk)
                        if total_tamano > 0:
                            porcentaje_descargado = (tamano_descargado / total_tamano) * 100
                            # Verificar si hemos alcanzado o superado el siguiente umbral de 10%
                            while porcentaje_descargado >= last_logged_percentage + 10:
                                last_logged_percentage += 10
                                # Asegurarse de no exceder el 100%
                                if last_logged_percentage > 100:
                                    last_logged_percentage = 100
                                logger.info(f"Descargado: {last_logged_percentage:.2f}%")
                        else:
                            # Si no se conoce el tamaño total, registrar cada chunk descargado
                            logger.info(f"Descargado: {tamano_descargado} bytes")
                
                # Al finalizar la descarga, asegurarse de registrar el 100% si aún no se ha hecho
                if total_tamano > 0 and last_logged_percentage < 100:
                    logger.info("Descargado: 100.00%")
        
        logger.info(f"Descarga completada: {nombre_archivo}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al descargar el archivo: {e}")
        return False
    except Exception as e:
        logger.error(f"Error al guardar el archivo: {e}")
        return False