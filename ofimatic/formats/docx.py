"""
Procesamiento específico de documentos DOCX (Office Open XML).
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Dict
import xml.etree.ElementTree as ET
import logging

from utils.i18n.safe import safe_gettext as _
from ofimatic.loader_officezip import read_multiple_zip_entries

logger = logging.getLogger(__name__)

_MAIN_XML = "word/document.xml"
_CORE_META = "docProps/core.xml"


def read_docx(path: str | Path) -> Dict[str, List[str]]:
    """
    Extrae los párrafos de un documento DOCX.
    Devuelve un dict con clave 'paragraphs'.
    """
    logger.info(_("docx_cargando"))
    try:
        data = read_multiple_zip_entries(path, [_MAIN_XML])
        xml = ET.fromstring(data[_MAIN_XML])

        namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paragraphs = []

        for p in xml.findall(".//w:p", namespace):
            texts = [t.text or "" for t in p.findall(".//w:t", namespace)]
            if texts:
                paragraphs.append("".join(texts))

        logger.info(_("docx_leido").format(parrafos=len(paragraphs)))
        return {"paragraphs": paragraphs}

    except Exception as exc:
        logger.error(_("docx_error_lectura").format(error=str(exc)))
        raise


def stats_docx(data: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Calcula estadísticas básicas del texto en DOCX:
    paragraphs, words, chars.
    """
    paragraphs = data.get("paragraphs", [])
    return {
        "paragraphs": len(paragraphs),
        "words": sum(len(p.split()) for p in paragraphs),
        "chars": sum(len(p) for p in paragraphs),
    }


def metadata_docx(path: str | Path) -> Dict[str, str]:
    """
    Lee metadatos básicos desde docProps/core.xml.
    """
    try:
        data = read_multiple_zip_entries(path, [_CORE_META])
        xml = ET.fromstring(data[_CORE_META])
        ns = {
            "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/"
        }

        def _get_text(xpath: str) -> str | None:
            el = xml.find(xpath, ns)
            return el.text.strip() if el is not None and el.text else None

        meta = {
            "title":            _get_text(".//dc:title"),
            "subject":          _get_text(".//dc:subject"),
            "creator":          _get_text(".//dc:creator"),
            "created":          _get_text(".//dcterms:created"),
            "modified":         _get_text(".//dcterms:modified"),
            "description":      _get_text(".//dc:description"),
            "keywords":         _get_text(".//cp:keywords"),
            "lastModifiedBy":   _get_text(".//cp:lastModifiedBy"),
        }

        return {k: v for k, v in meta.items() if v}

    except Exception as exc:
        logger.warning(_("docx_error_meta").format(error=str(exc)))
        return {}
