# 🔍 Detector de Tipo de Archivo

[Español](/README.md) | [English](/README/en.md) |

Una herramienta CLI en Python que identifica el tipo de archivo basado en su encabezado binario (magic numbers). Compatible con múltiples formatos, internacionalización (i18n), registro de logs y verbosidad configurable.

---

## 🚀 Características

- Detecta tipos de archivo leyendo los bytes del encabezado
- Soporta múltiples formatos (PDF, PNG, DOCX, XLSX, etc.)
- Soporte multilingüe
- Registro configurable (nivel de log y ruta)
- Códigos de salida claros para automatización

---

## 📦 Instalación

```bash
git clone https://github.com/CarlosDDCmx/ProcesArchivos.git
cd file-detector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

> Requiere Python 3.10 o superior

---

## 🔧 Uso

```bash
python cli/main.py <ruta_al_archivo> [opciones]
```

### ✅ Ejemplo

```bash
python cli/main.py ./samples/prueba.docx --bytes 32 --log-level DEBUG --enable-logging --lang es
```

---

## ⚙️ Opciones

| Opción              | Descripción                                                 |
| ------------------- | ----------------------------------------------------------- |
| `<archivo>`         | Ruta del archivo a analizar                                 |
| `--bytes <n>`       | Número de bytes del encabezado a leer (por defecto: 64)     |
| `--log-level`       | Nivel de registro (DEBUG, INFO, WARNING, ERROR, CRITICAL)   |
| `--enable-logging`  | Guarda un log en archivo (se crea automáticamente `.logs/`) |
| `--log-file <ruta>` | Ruta personalizada para guardar el log                      |
| `--lang <código>`   | Idioma para los mensajes (`en`, `es`)                       |
| `--quiet`           | Suprime los mensajes en la terminal (ideal para scripts)    |

---

## 🌐 Internacionalización (i18n)

Idiomas soportados:

* `en` – Inglés
* `es` – Español

```bash
python cli/main.py archivo.docx --lang es
```

Para agregar un nuevo idioma:

1. Crea un archivo en `core/i18n/lang/` llamado `<codigo>.json`
2. Usa como base el contenido de `es.json`
3. Ejecuta el programa con `--lang <codigo>`

---

## 📤 Códigos de salida

| Código | Significado                             |
| ------ | --------------------------------------- |
| 0      | Tipo de archivo detectado correctamente |
| 1      | Tipo de archivo desconocido             |
| 2      | Ocurrió un error                        |

---

## 📁 Estructura del Proyecto

```
.
├── cli/
│   └── main.py          # Interfaz CLI
├── core/
│   ├── detector.py      # Lógica de detección
│   ├── reader.py        # Lector de encabezado
│   ├── logger.py        # Utilidad de logs
│   └── i18n.py          # Soporte de idiomas
├── data/
│   └── signatures.json  # Archivo de firmas de encabezado
├── i18n/                # Carpeta con archivos (json) para cada idioma
├── .logs/               # Carpeta para logs (se crea automáticamente)
```

---
