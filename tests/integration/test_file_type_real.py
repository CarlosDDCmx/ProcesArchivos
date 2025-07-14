from detector.analyzer import detect_file_type

def test_real_pdf_detection(tmp_path):
    file = tmp_path / "test.pdf"
    file.write_bytes(b'%PDF-1.7 content...')
    result = detect_file_type(str(file))
    assert result["detected_type"].lower() in ["pdf document", "documento pdf"]
