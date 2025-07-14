from detector.heuristics import detect_with_heuristics

def test_heuristic_match_by_extension():
    entry = {
        "magic": "504B0304",
        "extensions": [".odt"],
        "mime_types": [],
        "detected_type": "OpenDocument Text"
    }
    header = b'\x50\x4B\x03\x04'
    result = detect_with_heuristics(header, "doc.odt", ".odt", None, [entry])
    assert result == "OpenDocument Text"

def test_heuristic_match_by_mime():
    entry = {
        "magic": "504B0304",
        "extensions": [],
        "mime_types": ["application/vnd.oasis.opendocument.spreadsheet"],
        "detected_type": "OpenDocument Spreadsheet"
    }
    result = detect_with_heuristics(
        b'\x50\x4B\x03\x04',
        "doc.ods",
        ".ods",
        "application/vnd.oasis.opendocument.spreadsheet",
        [entry]
    )
    assert result == "OpenDocument Spreadsheet"

def test_heuristic_no_match():
    result = detect_with_heuristics(
        b'\x00\x00\x00',
        "doc.unk",
        ".unk",
        "application/unknown",
        []
    )
    assert result is None
