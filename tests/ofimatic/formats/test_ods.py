from ofimatic.formats.ods import read_ods, stats_ods, metadata_ods
from unittest.mock import patch
from pathlib import Path

@patch("ofimatic.formats.ods.read_opendocument")
def test_read_ods(mock_read):
    mock_read.return_value = {"sheets": {"Hoja1": [["1", "2"]]}, "dims": {"Hoja1": (1, 2)}}
    result = read_ods(Path("archivo.ods"))
    assert "sheets" in result

@patch("ofimatic.formats.ods.stats_opendoc")
def test_stats_ods(mock_stats):
    mock_stats.return_value = {"sheets": 1, "total_cells": 2}
    result = stats_ods({"sheets": {"Hoja": [["A"]]}, "dims": {"Hoja": (1, 1)}})
    assert result["sheets"] == 1

@patch("ofimatic.formats.ods.metadata_opendoc")
def test_metadata_ods(mock_meta):
    mock_meta.return_value = {"creator": "Autor"}
    result = metadata_ods("archivo.ods")
    assert result["creator"] == "Autor"
