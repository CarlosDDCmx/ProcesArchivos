
# 🧠 Detector de Tipo de Archivo CLI

[Español](/README.md) | [English](/README/en.md)

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3130/)
[![Estado](https://img.shields.io/badge/estado-en%20desarrollo-yellow)](#)
[![Compatibilidad](https://img.shields.io/badge/i18n-es%2Fen-lightgrey)](#)

Aplicación CLI modular e internacionalizada para detectar y analizar documentos mediante la lectura de encabezados y contenidos internos.

---

## 🚀 Características

- 🔍 Detección precisa del tipo de archivo desde su cabecera binaria.
- 📖 Lectura de contenido textual desde documentos OpenDocument (`.odt`) y Office (`.docx`).
- 📊 Estadísticas detalladas de contenido (párrafos, palabras, celdas).
- 📑 Extracción de metadatos estándar (autor, fechas, título, etc.).
- 🧠 Registro automático de sesiones con memoria activa y persistente.
- 🌐 Soporte multilenguaje (`gettext`).
- 🧩 Arquitectura extensible basada en menús y comandos.

---

## 📁 Estructura del Proyecto

```

procesArchivos/
├── core/                    # Entrada principal (main.py)
├── detector/                # Detección binaria por encabezado
│   └── signatures.json      # Firmas mágicas por tipo
├── locale/                  # Archivos de mensajes para internacionalización
├── memory/                  # Sistema de eventos y registro
│   ├── events.py
│   ├── bus.py
│   ├── subscribers.py
│   └── __init__.py
├── menu/                    # Menús CLI
│   ├── menu.py              # Lógica de menú
│   ├── navigator.py         # Menús básicos
│   ├── commands/            # Integración de funciones
│   └── menus/               # Estructura de menú
├── ofimatic/                # Lectura y análisis de documentos
│   ├── formtas/             # Procesamiento de documentos específicos
│   ├── core_zip.py          # Núcleo común
│   ├── loader_officezip.py  # Comprobación de formatos office MS
│   └── loader_opendoc.py    # Comprobación de formatos open office
├── utils/                   # i18n, logging y utilidades
│   ├── i18n/
│   └── logger/
├── locale/                  # Traducciones
└── results/                 # Salidas de sesión en JSON

````

---

## ⚙️ Requisitos

- Python 3.13 o superior
- Uso exclusivo de bibliotecas estándar (`gettext`, `os`, `mimetypes`, `zipfile`, `xml.etree`, etc.)

---

## 🧪 Ejecución

Ejecuta desde la raíz del proyecto:

```bash
python core/main.py
````

Interactúa desde el menú:

```
🛠 Herramientas
--------------
0. 🔙 Volver
1. 🔎 Detectores
2. 📖 Procesar OpenDocument
m. Ver memoria
r. Ver resultados
s. 📂 Seleccionar archivo activo
x. Salir
```

Menú de Documentos:

```
📖 Documentos
------------
0. 🔙 Volver
1. 📄 Leer contenido
2. 📊 Obtener estadísticas
3. 📑 Leer metadatos
```

---

## 🧠 Ejemplo de Análisis

```text
📄 Introduce la ruta al archivo: informe.odt
🔢 ¿Cuántos bytes del encabezado deseas leer? (por defecto: 8): 16

✅ Resultado de la detección:
path: informe.odt
size: 1048183
header: 504b0304140000080000159c
header_bytes: 16
extension: .odt
mime_type: application/vnd.oasis.opendocument.text
detected_type: OpenDocument
```

---

## 🧠 Memoria y Resultados

Cada análisis genera:

* 🧠 Evento en memoria activa (accesible con `Ver memoria`)
* 📁 Archivo JSON en `results/<archivo>.json` con análisis simple
* 🔄 Selección de archivo activo para trabajar con distintos comandos

---

## 🌍 Internacionalización (i18n)

Este proyecto usa `gettext`.

### Para cambiar el idioma:

```bash
# Windows
set LANG=es_MX.UTF-8

# Linux/macOS
export LANG=es_MX.UTF-8
```

### Para agregar nuevos idiomas:

```bash
# Generar archivo .po
pygettext -d messages -o locale/fr/LC_MESSAGES/messages.po utils/i18n/safe.py

# Compilar traducción
msgfmt locale/fr/LC_MESSAGES/messages.po -o locale/fr/LC_MESSAGES/messages.mo
```
