# 🔍 File Type Detector

[Español](/README.md) | [English](/README/en.md) |

A Python CLI tool that identifies file types based on their binary header (magic numbers). Supports multiple formats, internationalization (i18n), logging, and configurable verbosity.

---

## 🚀 Features

- Detects file types by reading header bytes
- Supports multiple formats (PDF, PNG, DOCX, XLSX, etc.)
- Multilingual support
- Configurable logging (log level and path)
- Clear exit codes for automation

---

## 📦 Installation

```bash
git clone https://github.com/CarlosDDCmx/ProcesArchivos.git
cd ProcesArchivos
python3 -m venv <project_name>
source <project_name>/bin/activate
pip install -r requirements.txt
```

> Requires Python 3.10 or higher

---

## 🔧 Usage

```bash
python cli/main.py <file_path> [options]
```

### ✅ Example

```bash
python cli/main.py ./samples/test.docx --bytes 32 --log-level DEBUG --enable-logging --lang en
```

---

## ⚙️ Options

| Option              | Description                                                 |
| ------------------- | ----------------------------------------------------------- |
| `<file>`            | Path to the file to analyze                                 |
| `--bytes <n>`       | Number of header bytes to read (default: 64)                |
| `--log-level`       | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)       |
| `--enable-logging`  | Save log to file (automatically creates `.logs/`)           |
| `--log-file <path>` | Custom path to save the log file                            |
| `--lang <code>`     | Language for messages (`en`, `es`)                          |
| `--quiet`           | Suppress terminal messages (ideal for scripts)              |

---

## 🌐 Internationalization (i18n)

Supported languages:

* `en` – English
* `es` – Spanish

```bash
python cli/main.py file.docx --lang en
```

To add a new language:

1. Create a file in `core/i18n/lang/` named `<code>.json`
2. Use `es.json` as a base
3. Run the program with `--lang <code>`

---

## 📤 Exit codes

| Code | Meaning                             |
| ---- | ----------------------------------- |
| 0    | File type detected successfully     |
| 1    | Unknown file type                   |
| 2    | An error occurred                   |

---

## 📁 Project Structure

```
.
├── cli/
│   └── main.py          # CLI interface
├── core/
│   ├── detector.py      # Detection logic
│   ├── reader.py        # Header reader
│   ├── logger.py        # Log utility
│   └── i18n.py          # Language support
├── data/
│   └── signatures.json  # Header signatures file
├── i18n/                # Folder with (json) files for each language
├── .logs/               # Log folder (created automatically)
```

---