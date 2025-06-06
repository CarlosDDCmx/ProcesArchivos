import pytest
from core.detector import detect_from_header, load_signatures

def test_detect_zip_signature(tmp_path):
    dummy_zip = tmp_path / "sample.odt"
    with dummy_zip.open("wb") as f:
        f.write(b"PK\x03\x04")  # Firma ZIP
    
    firmas = load_signatures()
    result = detect_from_header(b"PK\x03\x04", str(dummy_zip), firmas)
    assert "ZIP" in result or "ODT" in result

def test_unknown_signature(tmp_path):
    file = tmp_path / "unknown.bin"
    file.write_bytes(b"\x00\x01\x02")
    
    firmas = load_signatures()
    result = detect_from_header(b"\x00\x01\x02", str(file), firmas)
    assert result is None
