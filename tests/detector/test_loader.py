import json
from unittest.mock import mock_open, patch
from detector.loader import load_signatures

def test_load_signatures_valid():
    fake_data = {
        "signatures": {
            "25504446": "PDF Document",
            "504B0304": "ZIP Archive"
        },
        "ambiguous_signatures": [
            {"magic": "504B0304", "extensions": [".zip"], "detected_type": "ZIP Archive"}
        ]
    }

    mocked_file = mock_open(read_data=json.dumps(fake_data))

    with patch("builtins.open", mocked_file):
        with patch("os.path.join", return_value="any/path/signatures.json"):
            signatures, ambiguous = load_signatures()

    assert signatures[b'%PDF'] == "PDF Document"
    assert signatures[b'PK\x03\x04'] == "ZIP Archive"
    assert ambiguous[0]["detected_type"] == "ZIP Archive"