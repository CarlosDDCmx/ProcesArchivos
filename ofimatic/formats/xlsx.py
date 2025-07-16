"""
Procesamiento específico de hojas de cálculo XLSX.
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict, List
import xml.etree.ElementTree as ET
import logging

from utils.i18n.safe import safe_gettext as _
from ofimatic.loader_officezip import read_multiple_zip_entries

logger = logging.getLogger(__name__)

_SHARED_STRINGS = "xl/sharedStrings.xml"
_SHEET_XML = "xl/worksheets/sheet1.xml"  # Solo lee la hoja1
_META_CORE = "docProps/core.xml"


def read_xlsx(path: str | Path) -> Dict[str, List[List[str]]]:
    """
    Extrae el contenido tabular de la primera hoja.
    Devuelve {"sheet1": matriz}.
    """
    logger.info(_("xlsx_cargando"))

    try:
        files = [_SHEET_XML, _SHARED_STRINGS]
        data = read_multiple_zip_entries(path, files)
        namespace = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        # Procesar sharedStrings si existen
        shared = []
        if _SHARED_STRINGS in data:
            root = ET.fromstring(data[_SHARED_STRINGS])
            shared = [t.text or "" for t in root.findall(".//a:t", namespace)]

        root = ET.fromstring(data[_SHEET_XML])
        rows: List[List[str]] = []

        for r in root.findall(".//a:row", namespace):
            cells = []
            for c in r.findall(".//a:c", namespace):
                v = c.find("a:v", namespace)
                if v is not None:
                    if c.attrib.get("t") == "s":
                        idx = int(v.text)
                        cells.append(shared[idx] if idx < len(shared) else "")
                    else:
                        cells.append(v.text or "")
                else:
                    cells.append("")
            rows.append(cells)

        logger.info(_("xlsx_leido_hojas").format(hojas=len(rows)))
        return {"sheet1": rows}

    except Exception as exc:
        logger.error(_("xlsx_error_lectura").format(error=str(exc)))
        raise


def stats_xlsx(data: Dict[str, List[List[str]]]) -> Dict[str, int]:
    """
    Cuenta filas, columnas y celdas.
    """
    sheet = data.get("sheet1", [])
    return {
        "rows": len(sheet),
        "cols": max(map(len, sheet), default=0),
        "cells": sum(len(row) for row in sheet),
    }


def metadata_xlsx(path: str | Path) -> Dict[str, str]:
    """
    Lee metadatos básicos desde docProps/core.xml.
    """
    try:
        data = read_multiple_zip_entries(path, [_META_CORE])
        xml = ET.fromstring(data[_META_CORE])

        ns = {
            "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/"
        }

        def _get(xpath: str) -> str | None:
            el = xml.find(xpath, ns)
            return el.text.strip() if el is not None and el.text else None

        meta = {
            "title":    _get(".//dc:title"),
            "creator":  _get(".//dc:creator"),
            "created":  _get(".//dcterms:created"),
            "modified": _get(".//dcterms:modified"),
        }

        return {k: v for k, v in meta.items() if v}

    except Exception as exc:
        logger.warning(_("xlsx_error_meta").format(error=str(exc)))
        return {}
