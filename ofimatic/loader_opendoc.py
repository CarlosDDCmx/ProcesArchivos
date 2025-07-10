"""
Lectura y análisis de documentos OpenDocument (ODT, ODS, ODP).

Funciones expuestas:
    • read_opendocument(path)            → Dict[str, Any]
    • stats_opendoc(data)                → Dict[str, int]
    • metadata_opendoc(path)             → Dict[str, str]
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

import logging
import xml.etree.ElementTree as ET
from zipfile import ZipFile, BadZipFile

from utils.i18n.safe import safe_gettext as _

logger = logging.getLogger(__name__)

# ── EXCEPCIÓN ──────────────────────────────────────────────
class OpenDocError(Exception):
    """Errores de lectura / análisis ODF."""

# ── CONSTANTES XML ─────────────────────────────────────────
NS_TEXT  = {"text":  "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}
NS_TABLE = {"table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0"}
NS_DRAW  = {"draw":  "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"}
NS_META  = {
    "dc":   "http://purl.org/dc/elements/1.1/",
    "meta": "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
}

_MAIN_XML = "content.xml"
_META_XML = "meta.xml"

# ── LOAD ─ lectura básica ──────────────────────────────────
def _read_zip_entry(path: Path, entry: str) -> bytes:
    try:
        with ZipFile(path) as zf:
            return zf.read(entry)
    except (BadZipFile, KeyError) as exc:
        raise OpenDocError(_("loader_error").format(error=str(exc))) from exc

def read_opendocument(path: str | Path) -> Dict[str, Any]:
    """
    Devuelve un dict inmutable con:
        • paragraphs : List[str]                (ODT / ODP)
        • tables     : List[ List[List[str]] ]  (ODT / ODP)
        • ole        : int                      (ODT / ODP)
        • sheets     : Dict[sheet → matrix]     (ODS)
        • dims       : Dict[sheet → (r, c)]     (ODS)
    """
    path = Path(path)
    logger.info(_("odf_cargando"))

    # --- abrir y parsear content.xml ---
    xml_bytes = _read_zip_entry(path, _MAIN_XML)
    root = ET.fromstring(xml_bytes)

    extension = path.suffix.lower()
    data: Dict[str, Any] = {}

    # 1) PÁRRAFOS (solo ODT / ODP)
    if extension in {".odt", ".odp"}:
        paragraphs = ["".join(el.itertext()) for el in root.findall(".//text:p", NS_TEXT)]
        data["paragraphs"] = paragraphs

    # 2) TABLAS genéricas (ODT) o HOJAS (ODS)
    if extension == ".odt":
        data["tables"] = _extract_odt_tables(root)
    elif extension == ".ods":
        sheets, dims = _extract_ods_sheets(root)
        data["sheets"] = sheets
        data["dims"] = dims

    # 3) OBJETOS EMBEBIDOS (draw:object)
    data["ole"] = len(root.findall(".//draw:object", NS_DRAW))

    logger.info(_("odf_leido").format(parrafos=len(data.get("paragraphs", []))))
    return data

# ── helpers ────────────────────────────────────────────────
def _extract_odt_tables(root: ET.Element) -> List[List[List[str]]]:
    """tabla → fila → celda (texto plano)."""
    tables = []
    for t in root.findall(".//table:table", NS_TABLE):
        rows = []
        for r in t.findall("table:table-row", NS_TABLE):
            cells = [
                "".join(c.itertext()) for c in r.findall("table:table-cell", NS_TABLE)
            ]
            rows.append(cells)
        tables.append(rows)
    return tables

def _extract_ods_sheets(root: ET.Element) -> Tuple[Dict[str, List[List[Any]]],
                                                   Dict[str, Tuple[int, int]]]:
    sheets: Dict[str, List[List[Any]]] = {}
    dims:   Dict[str, Tuple[int, int]] = {}
    for t in root.findall(".//table:table", NS_TABLE):
        name = t.attrib.get(f"{{{NS_TABLE['table']}}}name", "Sheet")
        matrix = []
        for r in t.findall("table:table-row", NS_TABLE):
            cells = [c.text or "" for c in r.findall("table:table-cell", NS_TABLE)]
            matrix.append(cells)
        sheets[name] = matrix
        dims[name] = (len(matrix), max(map(len, matrix)) if matrix else 0)
    return sheets, dims

# ── ESTADÍSTICAS ───────────────────────────────────────────
def stats_opendoc(data: Dict[str, Any]) -> Dict[str, int]:
    """
    Calcula:
        paragraphs, tables, sheets, ole, words, chars, total_cells
    """
    try:
        paragraphs = data.get("paragraphs", [])
        tables     = data.get("tables", [])
        sheets     = data.get("sheets", {})
        dims       = data.get("dims", {})

        return {
            "paragraphs": len(paragraphs),
            "tables":     len(tables),
            "sheets":     len(sheets),
            "ole":        data.get("ole", 0),
            "words":      sum(len(p.split()) for p in paragraphs),
            "chars":      sum(len(p)         for p in paragraphs),
            "total_cells": sum(r * c for r, c in dims.values()),
        }
    except Exception as exc:
        logger.error(_("odf_stats_error").format(error=str(exc)))
        raise OpenDocError from exc
    
# ── METADATOS ──────────────────────────────────────────────
def metadata_opendoc(path: str | Path) -> Dict[str, str]:
    """
    Extrae meta‑datos estándar de meta.xml:
        title, subject, description, author, initial_creator,
        created, modified, keywords, generator, editing_cycles,
        editing_duration
    """
    try:
        xml_bytes = _read_zip_entry(Path(path), _META_XML)
    except OpenDocError:
        return {}
    root = ET.fromstring(xml_bytes)

    def _first(xpath: str) -> str | None:
        """Devuelve el texto del primer nodo coincidente (o None)."""
        el = root.find(xpath, NS_META)
        return el.text.strip() if el is not None and el.text else None

    meta = {
        "title":            _first(".//dc:title"),
        "subject":          _first(".//dc:subject"),
        "description":      _first(".//dc:description"),
        "author":           _first(".//dc:creator"),
        "initial_creator":  _first(".//meta:initial-creator"),
        "created":          _first(".//meta:creation-date"),
        "modified":         _first(".//dc:date"),
        "keywords":         _first(".//meta:keyword"),
        "generator":        _first(".//meta:generator"),
        "editing_cycles":   _first(".//meta:editing-cycles"),
        "editing_duration": _first(".//meta:editing-duration"),
    }
    # Limpia pares None
    return {k: v for k, v in meta.items() if v}
