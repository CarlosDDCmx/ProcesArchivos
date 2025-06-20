# 🔍 File Type Detector 🧠 File Type Detector CLI

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3130/)
[![Status](https://img.shields.io/badge/status-in%20development-yellow)](#)  
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)  
[![i18n Support](https://img.shields.io/badge/i18n-es%2Fen-lightgrey)](#)  

[Español](/README.md) | [English](/README/en.md) |

A modular and internationalized CLI application to detect file types by reading binary headers.
---

## 🚀 Features

- 🔍 Accurate detection of file type from its header.
- 🌐 Multi-language support.
- 🧩 Extensible architecture based on menus.
- 🧪 Interactive and user-friendly CLI that’s easy to extend.

---

## 📌 Dependencies

* Python 3.13+
* Standard libraries (no external dependencies required).
* `gettext` for internationalization.

---

## 📁 Project Structure

```

procesArchivos/
├── core/                 # Entry point
│   └── main.py
├── menu/                 # Menu system
│   ├── menu.py
│   ├── navigator.py
│   ├── commands/
│   └── menus/
├── detector/             # Detection logic
│   ├── analyzer.py
│   ├── detector.py
│   ├── loader.py
│   ├── report.py
│   └── signatures.json
├── utils/                # General utilities
│   ├── i18n/             # For internationalization
│   └── logger/           # For debugging and logging
├── locale/               # Language files
│   └── es/LC/_MESSAGES/messages.mo
└── README.md

````

---

## ⚙️ Requirements

- Python 3.13 or higher
- Only standard libraries (`gettext`, `os`, `mimetypes`, etc.)

---

## 🧪 Execution

Follow the interactive menu instructions:

```
0. 🚪 Exit
1. 🛠 Tools
2. 👋 Greet
```

---

## 🧠 Detection Example

```text
📄 Enter the file path: example.pdf
🔢 How many header bytes would you like to read? (default: 8): 16

✅ Detection result:
path: example.pdf
size: 19345
header: 255044462d312e350a25d0d4c5d8
header_bytes: 16
extension: .pdf
mime_type: application/pdf
detected_type: PDF Document
```

---

## 🌍 Internationalization (i18n)

This project uses `gettext`. To change the language:

```bash
# Windows
set LANG=en_US.UTF-8

# Linux/macOS
export LANG=en_US.UTF-8
```

To add new languages:

```bash
pygettext -d messages -o locales/fr/LC_MESSAGES/messages.po utils/i18n.py
# Translate the .po file
msgfmt locales/fr/LC_MESSAGES/messages.po -o locales/fr/LC_MESSAGES/messages.mo
```