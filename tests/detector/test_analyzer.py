import pytest
from detector.analyzer import detect_from_header

def test_detect_exact_signature():
    signatures = {b'%PDF': "PDF Document"}
    header = b'%PDF-1.4'
    result = detect_from_header(header, "doc.pdf", ".pdf", "application/pdf", signatures, [])
    assert result == "PDF Document"

def test_detect_ambiguous_signature_by_extension():
    ambiguous = [
        {"magic": "504B0304", "extensions": [".odt"], "mime_types": [], "detected_type": "OpenDocument Text"}
    ]
    header = b'\x50\x4B\x03\x04' + b'extra'
    result = detect_from_header(header, "file.odt", ".odt", None, {}, ambiguous)
    assert result == "OpenDocument Text"

def test_detect_ambiguous_signature_by_mime():
    ambiguous = [
        {"magic": "504B0304", "extensions": [], "mime_types": ["application/vnd.oasis.opendocument.spreadsheet"], "detected_type": "OpenDocument Spreadsheet"}
    ]
    header = b'\x50\x4B\x03\x04'
    result = detect_from_header(header, "file.ods", ".ods", "application/vnd.oasis.opendocument.spreadsheet", {}, ambiguous)
    assert result == "OpenDocument Spreadsheet"

def test_detect_with_heuristics_fallback(monkeypatch):
    from detector import analyzer

    def fake_heuristics(*args, **kwargs):
        return "Detected via heuristics"

    monkeypatch.setattr(analyzer, "detect_with_heuristics", fake_heuristics)

    result = analyzer.detect_from_header(
        header=b'\x00\x00\x00',
        file_path="unknown.xyz",
        extension=".xyz",
        mime_type="application/xyz",
        signatures={},
        ambiguous_signatures=[],
    )
    assert result == "Detected via heuristics"