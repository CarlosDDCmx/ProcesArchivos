from ofimatic.formats.odt import read_odt, stats_odt, metadata_odt
from ofimatic.loader_opendoc import read_opendocument, stats_opendoc, metadata_opendoc
from unittest.mock import patch
from pathlib import Path

@patch("ofimatic.formats.odt.read_opendocument")
def test_read_odt(mock_read):
    expected = {"paragraphs": ["Hola mundo"]}
    mock_read.return_value = expected
    result = read_odt(Path("documento.odt"))
    assert result == expected

@patch("ofimatic.formats.odt.stats_opendoc")
def test_stats_odt(mock_stats):
    mock_stats.return_value = {"paragraphs": 1, "words": 2}
    data = {"paragraphs": ["Uno dos"]}
    result = stats_odt(data)
    assert result["paragraphs"] == 1

@patch("ofimatic.formats.odt.metadata_opendoc")
def test_metadata_odt(mock_meta):
    mock_meta.return_value = {"title": "Documento"}
    result = metadata_odt("documento.odt")
    assert result["title"] == "Documento"
