"""
Manejo de archivos ZIP de Office (DOCX, XLSX, PPTX).
Incluye funciones utilitarias de carga comunes.
"""

from __future__ import annotations
from typing import Dict
from pathlib import Path
from zipfile import ZipFile, BadZipFile
from utils.i18n.safe import safe_gettext as _
import logging

logger = logging.getLogger(__name__)

def read_multiple_zip_entries(path: str | Path, entries: list[str], workers: int = 2) -> Dict[str, bytes]:
    """
    Lee múltiples archivos internos de un contenedor ZIP (DOCX, XLSX, etc.)
    Devuelve: {nombre_entry → contenido_bytes}
    """
    path = Path(path)
    try:
        with ZipFile(path) as zf:
            return {
                entry: zf.read(entry)
                for entry in entries if entry in zf.namelist()
            }
    except BadZipFile as exc:
        logger.error(_("zip_error_invalido").format(error=str(exc)))
        raise RuntimeError(_("zip_error_invalido").format(error=str(exc)))
    except Exception as exc:
        logger.error(_("zip_error_lectura").format(path=path, error=str(exc)))
        raise RuntimeError(_("zip_error_lectura").format(path=path, error=str(exc)))