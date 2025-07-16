import pytest
import xml.etree.ElementTree as ET
from ofimatic.formats.docx import read_docx, stats_docx, metadata_docx
from ofimatic.loader_officezip import read_multiple_zip_entries
from pathlib import Path
from unittest.mock import patch

from tests.temp_files import TEMP_DIR

# ─── Setup de archivo DOCX simulado ──────────────────────────

DOCX_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>Primer párrafo</w:t></w:r></w:p>
    <w:p><w:r><w:t>Segundo párrafo</w:t></w:r></w:p>
  </w:body>
</w:document>
'''

DOCX_META = '''<?xml version="1.0" encoding="UTF-8"?>
<cp:coreProperties 
    xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/">
  <dc:title>Documento de prueba</dc:title>
  <dc:creator>Autor</dc:creator>
  <dcterms:created>2023-01-01T00:00:00Z</dcterms:created>
</cp:coreProperties>
'''

@pytest.fixture
def fake_docx_file(tmp_path):
    zip_path = tmp_path / "fake.docx"
    import zipfile
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("word/document.xml", DOCX_XML)
        zf.writestr("docProps/core.xml", DOCX_META)
    return zip_path

# ─── Pruebas de lectura ─────────────────────────────────────

def test_read_docx(fake_docx_file):
    result = read_docx(fake_docx_file)
    assert "paragraphs" in result
    assert result["paragraphs"] == ["Primer párrafo", "Segundo párrafo"]

# ─── Pruebas de lectura: error ──────────────────────────────
from unittest.mock import patch

@patch("ofimatic.formats.docx.read_multiple_zip_entries", side_effect=RuntimeError("fallo"))
def test_read_docx_error_logged(mock_read, fake_docx_file):
    with pytest.raises(RuntimeError):
        read_docx(fake_docx_file)

# ─── Pruebas de estadísticas ────────────────────────────────

def test_stats_docx(fake_docx_file):
    result = read_docx(fake_docx_file)
    stats = stats_docx(result)
    assert stats["paragraphs"] == 2
    assert stats["words"] == 4
    assert stats["chars"] == len("Primer párrafoSegundo párrafo")

# ─── Pruebas de metadatos ───────────────────────────────────

def test_metadata_docx(fake_docx_file):
    meta = metadata_docx(fake_docx_file)
    assert meta["title"] == "Documento de prueba"
    assert meta["creator"] == "Autor"
    assert meta["created"] == "2023-01-01T00:00:00Z"

# ─── Pruebas de metadatos: docx incompleto ──────────────────

@patch("ofimatic.formats.docx.read_multiple_zip_entries")
def test_metadata_docx_incomplete(mock_read):
    mock_read.return_value = {
        "docProps/core.xml": b"""
        <cp:coreProperties
            xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
            xmlns:dc="http://purl.org/dc/elements/1.1/">
            <dc:title></dc:title>
            <dc:creator/>
        </cp:coreProperties>
        """
    }
    meta = metadata_docx("archivo.docx")
    assert meta == {}  # Nada debe agregarse si está vacío o mal formado

# ─── Pruebas de metadatos: docx error ───────────────────────

@patch("ofimatic.formats.docx.read_multiple_zip_entries", side_effect=Exception("fallo"))
def test_metadata_docx_error_logged(mock_read):
    meta = metadata_docx("archivo.docx")
    assert meta == {}