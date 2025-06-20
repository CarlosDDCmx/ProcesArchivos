# 🧠 Detector de Tipo de Archivo CLI
[Español](/README.md) | [English](/README/en.md) |

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3130/)
[![Estado](https://img.shields.io/badge/estado-en%20desarrollo-yellow)](#)
[![Licencia](https://img.shields.io/badge/licencia-MIT-green)](LICENSE)
[![Compatibilidad](https://img.shields.io/badge/i18n-es%2Fen-lightgrey)](#)

Aplicación CLI modular e internacionalizada para detectar tipos de archivo mediante la lectura de encabezados binarios.
---

## 🚀 Características

- 🔍 Detección precisa del tipo de archivo a partir de su cabecera.
- 🌐 Soporte multiidioma.
- 🧩 Arquitectura extensible basada en menús.
- 🧪 CLI interactiva fácil de usar y ampliar.

---

## 📌 Dependencias

* Python 3.13+
* Librerías estándar (no necesita dependencias externas).
* `gettext` para internacionalización.

---

## 📁 Estructura del Proyecto

```

procesArchivos/
├── core/                 # Punto de entrada
│   └── main.py
├── menu/                 # Sistema de menús
│   ├── menu.py
│   ├── navigator.py
│   ├── commands/
│   └── menus/
├── detector/             # Lógica de detección
│   ├── analyzer.py
│   ├── detector.py
│   ├── loader.py
│   ├── report.py
│   └── signatures.json
├── utils/                # Utilidades generales
│   ├── i18n/             # Para internacionalización
│   └── logger/           # Para depuración y registros
├── locale/               # Archivos para cada idiomas
│   └── es/LC/_MESSAGES/messages.mo
└── README.md

````

---

## ⚙️ Requisitos

- Python 3.13 o superior
- Solo bibliotecas estándar (`gettext`, `os`, `mimetypes`, etc.)

---

## 🧪 Ejecución

Sigue las instrucciones del menú interactivo:

```
0. 🚪 Salir
1. 🛠 Herramientas
2. 👋 Saludar
```

---

## 🧠 Ejemplo de Detección

```text
📄 Introduce la ruta al archivo: ejemplo.pdf
🔢 ¿Cuántos bytes del encabezado deseas leer? (por defecto: 8): 16

✅ Resultado de la detección:
path: ejemplo.pdf
size: 19345
header: 255044462d312e350a25d0d4c5d8
header_bytes: 16
extension: .pdf
mime_type: application/pdf
detected_type: Documento PDF
```

---

## 🌍 Internacionalización (i18n)

Este proyecto utiliza `gettext`. Para cambiar el idioma:

```bash
# Windows
set LANG=es_MX.UTF-8

# Linux/macOS
export LANG=es_MX.UTF-8
```

Para agregar nuevos idiomas:

```bash
pygettext -d messages -o locales/fr/LC_MESSAGES/messages.po utils/i18n.py
# Traducir el archivo .po
msgfmt locales/fr/LC_MESSAGES/messages.po -o locales/fr/LC_MESSAGES/messages.mo
```
