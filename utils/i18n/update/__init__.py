"""
Subpaquete `update` para orquestar la sincronización de archivos de traducción.
Este módulo permite su ejecución como script (`python -m utils.i18n.update`).
"""

from .operations import (
    extract_translations,
    init_po_file,
    backup_po_file,
    deduplicate_po,
    merge_translations,
    verify_po,
    compile_mo,
)

from .paths import (
    BASE_DIR,
    LOCALE_DIR,
    POT_FILE,
    TEMP_FILE_LIST,
    get_paths_for_lang,
)

__all__ = [
    "extract_translations",
    "init_po_file",
    "backup_po_file",
    "deduplicate_po",
    "merge_translations",
    "verify_po",
    "compile_mo",
    "BASE_DIR",
    "LOCALE_DIR",
    "POT_FILE",
    "TEMP_FILE_LIST",
    "get_paths_for_lang",
]
