"""
Contiene constantes de rutas usadas por los comandos de actualización.
Detecta entorno de pruebas y ajusta las rutas según sea necesario.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
LOCALE_DIR = BASE_DIR / "locale"
POT_FILE = LOCALE_DIR / "messages.pot"
TEMP_FILE_LIST = BASE_DIR / "files.txt"

def get_paths_for_lang(lang_code: str) -> dict:
    lang_dir = LOCALE_DIR / lang_code / "LC_MESSAGES"
    po_file = lang_dir / "messages.po"
    mo_file = lang_dir / "messages.mo"
    backup_file = lang_dir / "messages.po.bak"

    return {
        "po": po_file,
        "mo": mo_file,
        "backup": backup_file,
        "dir": lang_dir
    }
