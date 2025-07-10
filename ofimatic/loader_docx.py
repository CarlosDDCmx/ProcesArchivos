"""
Lectura y análisis de documentos DOCX (Microsoft Word).

Funciones expuestas:
    • read_docx(path)                     → Dict[str, Any]
    • stats_docx(data)                   → Dict[str, int]
    • metadata_docx(path)                → Dict[str, str]
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from zipfile import ZipFile, BadZipFile
import logging

from utils.i18n.safe import safe_gettext as _
from .core_zip import read_multiple_zip_entries

logger = logging.getLogger(__name__)

# ── CONSTANTES ─────────────────────────────────────────────
_DOCX_MAIN_XML = "word/document.xml"
_DOCX_META_XML = "docProps/core.xml"

NS_W = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
NS_META = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dcterms": "http://purl.org/dc/terms/",
}

# ── LECTURA DE DOCUMENTO ──────────────────────────────────
def _extract_paragraphs(xml_bytes: bytes) -> List[str]:
    """Devuelve los párrafos de un documento DOCX (como texto plano)."""
    root = ET.fromstring(xml_bytes)
    paragraphs: list[str] = []
    for p in root.findall(".//w:p", NS_W):
        runs = [t.text or "" for t in p.findall(".//w:t", NS_W)]
        if runs:
            paragraphs.append("".join(runs))
    return paragraphs


def read_docx(path: str | Path, workers: int = 4) -> Dict[str, Any]:
    """
    Lee un archivo DOCX y devuelve un diccionario con:
        • paragraphs: List[str]
        • ole: int (no implementado, siempre 0 por ahora)
    """
    logger.info(_("docx_cargando"))
    try:
        data = read_multiple_zip_entries(path, [_DOCX_MAIN_XML], workers=workers)
        paragraphs = _extract_paragraphs(data[_DOCX_MAIN_XML])

        logger.info(_("docx_leido").format(parrafos=len(paragraphs)))
        return {
            "paragraphs": paragraphs,
            "ole": 0,  # No implementado aún
        }
    except Exception as exc:
        message = _("docx_error_lectura").format(error=str(exc))
        logger.error(message)
        raise

# ── ESTADÍSTICAS ──────────────────────────────────────────
def stats_docx(data: Dict[str, Any]) -> Dict[str, int]:
    """
    Calcula estadísticas a partir de los datos del DOCX:
        paragraphs, words, chars, ole, tables, sheets, total_cells
    """
    try:
        paragraphs = data.get("paragraphs", [])
        return {
            "paragraphs": len(paragraphs),
            "words":      sum(len(p.split()) for p in paragraphs),
            "chars":      sum(len(p)         for p in paragraphs),
            "ole":        data.get("ole", 0),
            "tables":     0,
            "sheets":     0,
            "total_cells": 0,
        }
    except Exception as exc:
        logger.error(_("docx_stats_error").format(error=str(exc)))
        raise

# ── METADATOS ─────────────────────────────────────────────
def metadata_docx(path: str | Path) -> Dict[str, str]:
    """
    Extrae metadatos estándar de un archivo DOCX:
        title, author, last_modified_by, created, modified
    """
    try:
        with ZipFile(path) as zf:
            with zf.open(_DOCX_META_XML) as f:
                root = ET.parse(f).getroot()

        def _get(tag: str) -> str | None:
            el = root.find(f".//{tag}", NS_META)
            return el.text.strip() if el is not None and el.text else None

        meta = {
            "title":             _get("dc:title"),
            "author":            _get("dc:creator"),
            "last_modified_by":  _get("cp:lastModifiedBy"),
            "created":           _get("dcterms:created"),
            "modified":          _get("dcterms:modified"),
        }
        return {k: v for k, v in meta.items() if v}
    except (BadZipFile, KeyError, ET.ParseError) as exc:
        logger.warning(_("docx_meta_error").format(error=str(exc)))
        return {}
