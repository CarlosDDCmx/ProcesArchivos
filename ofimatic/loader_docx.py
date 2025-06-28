from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET
import logging

from utils.i18n.safe import safe_gettext as _
from .core_zip import read_multiple_zip_entries

logger = logging.getLogger(__name__)

_DOCX_MAIN_XML = "word/document.xml"


def _extract_paragraphs(xml_bytes: bytes) -> List[str]:
    """Devuelve los párrafos de un documento DOCX."""
    namespace = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    }
    root = ET.fromstring(xml_bytes)
    paragraphs: list[str] = []
    for p in root.findall(".//w:p", namespace):
        runs = [t.text or "" for t in p.findall(".//w:t", namespace)]
        if runs:
            paragraphs.append("".join(runs))
    return paragraphs


def read_docx(path: str | Path, workers: int = 4) -> List[str]:
    """Lee un archivo DOCX y devuelve texto por párrafos."""
    logger.info(_("docx_cargando"))
    try:
        data = read_multiple_zip_entries(path, [_DOCX_MAIN_XML], workers=workers)
        paragraphs = _extract_paragraphs(data[_DOCX_MAIN_XML])
        logger.info(_("docx_leido").format(parrafos=len(paragraphs)))
        return paragraphs
    except Exception as exc:
        message = _("docx_error_lectura").format(error=str(exc))
        logger.error(message)
        raise
