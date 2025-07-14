import tempfile
from detector import detector

def test_detect_from_known_signature():
    signatures = {b'%PDF': "PDF Document"}
    result = detector.detect_from_header(b'%PDF-1.4', signatures)
    assert result == "PDF Document"

def test_detect_from_unknown_signature():
    result = detector.detect_from_header(b'\x00\x00', {})
    assert result.lower() == "desconocido"

def test_detect_file_type_basic(tmp_path, monkeypatch):
    test_file = tmp_path / "test.pdf"
    test_file.write_bytes(b'%PDF-1.4...somecontent')

    monkeypatch.setattr("detector.detector.MAGIC_HEADERS", {b'%PDF': "PDF Document"})

    result = detector.detect_file_type(str(test_file))
    assert result["detected_type"].lower() in ["pdf document", "documento pdf"]