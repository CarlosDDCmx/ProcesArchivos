import pytest
from ofimatic.formats.xlsx import read_xlsx, stats_xlsx, metadata_xlsx
from ofimatic.loader_officezip import read_multiple_zip_entries
from unittest.mock import patch
from pathlib import Path

# ─── Pruebas de lectura ─────────────────────────────────────
@patch("ofimatic.formats.xlsx.read_multiple_zip_entries")
def test_read_xlsx_valid(mock_read):
    path = Path("archivo.xlsx")
    mock_read.return_value = {
        "xl/worksheets/sheet1.xml": b"""
        <worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
            <sheetData>
                <row><c><v>1</v></c><c t="s"><v>0</v></c></row>
                <row><c><v>2</v></c></row>
            </sheetData>
        </worksheet>
        """,
        "xl/sharedStrings.xml": b"""
        <sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
            <si><t>Texto</t></si>
        </sst>
        """,
    }
    result = read_xlsx(path)
    assert "sheet1" in result
    assert result["sheet1"] == [["1", "Texto"], ["2"]]

# ─── Pruebas de lectura: error ──────────────────────────────
@patch("ofimatic.formats.xlsx.read_multiple_zip_entries", side_effect=RuntimeError("fallo"))
def test_read_xlsx_error_logged(mock_read):
    with pytest.raises(RuntimeError):
        read_xlsx(Path("inexistente.xlsx"))


# ─── Pruebas de estadísticas ────────────────────────────────
def test_stats_xlsx_counts():
    data = {
        "sheet1": [["A", "B"], ["C", "D", "E"], ["F"]]
    }
    stats = stats_xlsx(data)
    assert stats["rows"] == 3
    assert stats["cols"] == 3
    assert stats["cells"] == 6

# ─── Pruebas de lectura multiple ───────────────────────────
@patch("ofimatic.formats.xlsx.read_multiple_zip_entries")
def test_metadata_xlsx_returns_expected(mock_read):
    mock_read.return_value = {
        "docProps/core.xml": b"""
        <cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>Archivo</dc:title>
            <dc:creator>Autor</dc:creator>
            <dcterms:created>2024-01-01</dcterms:created>
            <dcterms:modified>2024-01-02</dcterms:modified>
        </cp:coreProperties>
        """
    }
    meta = metadata_xlsx("archivo.xlsx")
    assert meta["title"] == "Archivo"
    assert meta["creator"] == "Autor"
    assert meta["created"] == "2024-01-01"
    assert meta["modified"] == "2024-01-02"

# ─── Pruebas de metadatos ───────────────────────────────────
@patch("ofimatic.formats.xlsx.read_multiple_zip_entries", side_effect=Exception("fallo"))
def test_metadata_xlsx_error_logged(mock_read):
    meta = metadata_xlsx("archivo.xlsx")
    assert meta == {}

# ─── Pruebas de metadatos: incompleto────────────────────────
@patch("ofimatic.formats.xlsx.read_multiple_zip_entries")
def test_metadata_xlsx_incomplete(mock_read):
    mock_read.return_value = {
        "docProps/core.xml": b"""
        <cp:coreProperties
            xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
            xmlns:dc="http://purl.org/dc/elements/1.1/">
            <dc:title></dc:title>
        </cp:coreProperties>
        """
    }
    meta = metadata_xlsx("archivo.xlsx")
    assert meta == {}