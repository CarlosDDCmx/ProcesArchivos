import pytest
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from ofimatic.loader_opendoc import (
    read_opendocument,
    stats_opendoc,
    metadata_opendoc,
    OpenDocError,
)
from zipfile import ZipFile

TEMP_DIR = Path("tests/temp_files")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────────────────────
# Utilidad para crear ZIP OpenDocument artificial
# ──────────────────────────────────────────────────────────────
def create_fake_odt(path: Path, content: str, meta: str = ""):
    with ZipFile(path, "w") as z:
        z.writestr("content.xml", content)
        if meta:
            z.writestr("meta.xml", meta)

# ──────────────────────────────────────────────────────────────
# Párrafo y tabla de prueba para ODT válido
# ──────────────────────────────────────────────────────────────
VALID_ODT_CONTENT = """<?xml version="1.0"?>
<document xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
          xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
          xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0">
    <text:p>Este es un párrafo.</text:p>
    <table:table>
        <table:table-row>
            <table:table-cell><text:p>A1</text:p></table:table-cell>
            <table:table-cell><text:p>B1</text:p></table:table-cell>
        </table:table-row>
    </table:table>
    <draw:object />
</document>
"""

VALID_META = """<?xml version="1.0"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0">
  <office:meta>
    <dc:title>Documento de Prueba</dc:title>
    <meta:initial-creator>Autor</meta:initial-creator>
  </office:meta>
</office:document-meta>
"""

# ──────────────────────────────────────────────────────────────
# TEST: Lectura exitosa de ODT válido
# ──────────────────────────────────────────────────────────────
def test_read_opendocument_valid_odt():
    file = TEMP_DIR / "doc_valido.odt"
    create_fake_odt(file, VALID_ODT_CONTENT)
    data = read_opendocument(file)
    assert "paragraphs" in data
    assert "tables" in data
    assert "ole" in data
    assert data["paragraphs"] == ["Este es un párrafo.", "A1", "B1"]
    assert data["ole"] == 1

# ──────────────────────────────────────────────────────────────
# TEST: Manejo de ZIP corrupto
# ──────────────────────────────────────────────────────────────
def test_read_opendocument_invalid_zip():
    file = TEMP_DIR / "zip_malo.odt"
    file.write_bytes(b"No es un ZIP")

    with pytest.raises(OpenDocError):
        read_opendocument(file)

# ──────────────────────────────────────────────────────────────
# TEST: Estadísticas básicas
# ──────────────────────────────────────────────────────────────
def test_stats_opendoc_counts_correctly():
    data = {
        "paragraphs": ["Uno dos", "Tres cuatro"],
        "tables": [["fila1"]],
        "sheets": {"S1": [["a"] * 2] * 3},
        "dims": {"S1": (3, 2)},
        "ole": 2
    }
    stats = stats_opendoc(data)
    assert stats["paragraphs"] == 2
    assert stats["tables"] == 1
    assert stats["sheets"] == 1
    assert stats["ole"] == 2
    assert stats["words"] == 4
    assert stats["chars"] == sum(len(p) for p in data["paragraphs"])
    assert stats["total_cells"] == 6

# ──────────────────────────────────────────────────────────────
# TEST: Metadatos válidos
# ──────────────────────────────────────────────────────────────
def test_metadata_opendoc_valid():
    file = TEMP_DIR / "doc_meta.odt"
    create_fake_odt(file, VALID_ODT_CONTENT, VALID_META)
    meta = metadata_opendoc(file)
    assert meta.get("title") == "Documento de Prueba"
    assert meta.get("initial_creator") == "Autor"

# ──────────────────────────────────────────────────────────────
# TEST: Metadatos ausentes
# ──────────────────────────────────────────────────────────────
def test_metadata_opendoc_missing_meta():
    file = TEMP_DIR / "doc_sin_meta.odt"
    create_fake_odt(file, VALID_ODT_CONTENT)
    meta = metadata_opendoc(file)
    assert meta == {}
