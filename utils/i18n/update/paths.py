"""
Contiene constantes de rutas usadas por los comandos de actualización.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
LOCALE_DIR = BASE_DIR / "locale"
POT_FILE = LOCALE_DIR / "messages.pot"
PO_FILE = LOCALE_DIR / "es" / "LC_MESSAGES" / "messages.po"
MO_FILE = LOCALE_DIR / "es" / "LC_MESSAGES" / "messages.mo"
TEMP_FILE_LIST = BASE_DIR / "files.txt"
BACKUP_FILE = PO_FILE.with_name("messages.po.bak")