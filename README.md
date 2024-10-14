# Padrón Reducido SUNAT

[![License](https://img.shields.io/github/license/JoeApaza/Patron_Reducido_SUNAT)](https://github.com/JoeApaza/Patron_Reducido_SUNAT/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![GitHub Repo Stars](https://img.shields.io/github/stars/JoeApaza/Patron_Reducido_SUNAT?style=social)](https://github.com/JoeApaza/Patron_Reducido_SUNAT)

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración de Logging](#configuración-de-logging)
- [Manejo de Errores](#manejo-de-errores)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Descripción

**Padrón Reducido SUNAT** es una herramienta desarrollada en Python diseñada para automatizar la descarga y procesamiento del Padrón Reducido de RUC proporcionado por la Superintendencia Nacional de Aduanas y de Administración Tributaria (SUNAT) de Perú. Este proyecto facilita la obtención de datos actualizados, asegurando eficiencia y precisión en el manejo de grandes volúmenes de información.

## Características

- **Automatización de Descargas**: Accede y descarga automáticamente el archivo ZIP del Padrón Reducido desde la página oficial de SUNAT.
- **Procesamiento Eficiente**: Utiliza técnicas de lectura en chunks para manejar archivos de gran tamaño sin comprometer la memoria.
- **Registro Detallado**: Implementa un sistema de logging que registra cada paso del proceso, facilitando la trazabilidad y el diagnóstico.
- **Manejo de Errores**: Identifica y maneja líneas problemáticas durante el procesamiento, asegurando la integridad de los datos.
- **Generación de Muestras**: Guarda muestras de los datos procesados en archivos Excel para una rápida revisión.

## Instalación

### Prerrequisitos

- **Python 3.8** o superior
- **pip** (Gestor de paquetes de Python)

### Clonar el Repositorio

```bash
git clone https://github.com/JoeApaza/Patron_Reducido_SUNAT.git
cd Patron_Reducido_SUNAT
```

### Crear un Entorno Virtual (Opcional pero Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Instalar las Dependencias

```bash
pip install -r requirements.txt
```

> **Nota**: Si el archivo `requirements.txt` no existe, puedes instalar las dependencias manualmente:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

## Uso

El proyecto está dividido en tres archivos principales:

1. **`descargar_zip.py`**: Contiene las funciones para acceder a la página de SUNAT, extraer la fecha de actualización y el enlace de descarga, y descargar el archivo ZIP.
2. **`procesar_zip.py`**: Incluye las funciones para abrir el archivo ZIP, contar las filas, procesar el archivo en chunks, manejar columnas adicionales y guardar una muestra de los datos.
3. **`main.py`**: Orquesta el flujo completo del programa, llamando a las funciones de los otros dos módulos.

### Ejecutar el Programa

```bash
python main.py
```

> **Nota**: Asegúrate de estar en el directorio raíz del proyecto donde se encuentran los archivos `main.py`, `descargar_zip.py` y `procesar_zip.py`.

## Estructura del Proyecto

```
Patron_Reducido_SUNAT/
├── descargar_zip.py
├── procesar_zip.py
├── main.py
├── requirements.txt
├── app.log
├── procesamiento.log
├── muestra_datos.xlsx
└── README.md
```

- **`descargar_zip.py`**: Módulo para descargar el archivo ZIP desde SUNAT.
- **`procesar_zip.py`**: Módulo para procesar el archivo ZIP descargado.
- **`main.py`**: Archivo principal que ejecuta el flujo completo.
- **`requirements.txt`**: Lista de dependencias del proyecto.
- **`app.log`**: Archivo de log principal donde se registran los eventos del programa.
- **`procesamiento.log`**: Archivo de log específico para el procesamiento del ZIP.
- **`muestra_datos.xlsx`**: Archivo Excel que contiene una muestra de los datos procesados.
- **`README.md`**: Documento de documentación del proyecto.

## Configuración de Logging

El sistema de logging está configurado para registrar eventos tanto en la consola como en archivos de log. Cada ejecución del programa sobrescribe el archivo `app.log` para mantener únicamente los registros de la última ejecución y utiliza la codificación UTF-8.

### Configuración en `main.py`

```python
import logging

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
```

- **`level=logging.INFO`**: Define el nivel de severidad mínima de los mensajes que se registrarán.
- **`format`**: Especifica el formato de los mensajes de log, incluyendo la fecha, nivel y mensaje.
- **`handlers`**:
  - **`FileHandler`**: Registra los mensajes en `app.log`, sobrescribiendo el archivo en cada ejecución y usando codificación UTF-8.
  - **`StreamHandler`**: Muestra los mensajes en la consola en tiempo real.

## Manejo de Errores

El programa está diseñado para manejar y registrar errores de manera eficiente:

- **Errores en la descarga**: Si la descarga del archivo ZIP falla, se registra un error y el programa termina.
- **Errores en el procesamiento**: Durante el procesamiento del archivo ZIP, las líneas problemáticas se registran y se omiten, asegurando que el resto de los datos se procesen correctamente.
- **Comparación de filas**: Al final del proceso, el programa compara el número de filas en el archivo original con las filas en el DataFrame procesado, registrando cualquier discrepancia.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto, por favor sigue los siguientes pasos:

1. **Fork** este repositorio.
2. **Crea una rama** para tu característica (`git checkout -b feature/nueva-caracteristica`).
3. **Commit** tus cambios (`git commit -m 'Añadir nueva característica'`).
4. **Push** a la rama (`git push origin feature/nueva-caracteristica`).
5. **Abre un Pull Request**.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](https://github.com/JoeApaza/Patron_Reducido_SUNAT/blob/main/LICENSE) para más detalles.

## Contacto

Para consultas o más información, puedes contactarme a través de:

- **Correo Electrónico**: [joemapaza97@gmail.com](mailto:joemapaza97@gmail.com)
- **Repositorio GitHub**: [https://github.com/JoeApaza/Patron_Reducido_SUNAT](https://github.com/JoeApaza/Patron_Reducido_SUNAT)

---

¡Gracias por utilizar **Padrón Reducido SUNAT**! Espero que esta herramienta te sea de gran ayuda en tu gestión de datos tributarios.
