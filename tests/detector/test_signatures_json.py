import json
import os

def test_signatures_json_is_valid():
    path = os.path.join(os.path.dirname(__file__), "..", "..", "detector", "signatures.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    assert "signatures" in data
    assert isinstance(data["signatures"], dict)
    assert "ambiguous_signatures" in data
