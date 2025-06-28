from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET
import logging

from utils.i18n.safe import safe_gettext as _
from .core_zip import read_multiple_zip_entries

logger = logging.getLogger(__name__)

# Mapeo extensión → archivo XML principal
_ODF_MAIN_XML = {
    ".odt": "content.xml",
    ".ods": "content.xml",
    ".odp": "content.xml",
}


def _extract_paragraphs(xml_bytes: bytes) -> List[str]:
    """Devuelve párrafos de texto plano desde un fragmento XML OpenDocument."""
    namespace = {"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}
    root = ET.fromstring(xml_bytes)
    paragraphs: list[str] = []
    for element in root.findall(".//text:p", namespace):
        paragraphs.append("".join(element.itertext()))
    return paragraphs


def read_opendocument(path: str | Path, workers: int = 4) -> List[str]:
    """Lee un archivo OpenDocument y retorna la lista de párrafos."""
    logger.info(_("odf_cargando"))
    path = Path(path)
    extension = path.suffix.lower()
    if extension not in _ODF_MAIN_XML:
        message = _("odf_error_formato").format(ext=extension)
        logger.error(message)
        raise ValueError(message)

    main_xml = _ODF_MAIN_XML[extension]
    data = read_multiple_zip_entries(path, [main_xml], workers=workers)
    paragraphs = _extract_paragraphs(data[main_xml])
    logger.info(_("odf_leido").format(parrafos=len(paragraphs)))
    return paragraphs
