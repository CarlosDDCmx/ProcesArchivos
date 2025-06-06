import pytest
from core.reader import read_file_header

def test_read_valid_file(tmp_path):
    dummy_file = tmp_path / "test.bin"
    dummy_file.write_bytes(b"\xDE\xAD\xBE\xEF")
    
    result = read_file_header(str(dummy_file), 2)
    assert result == b"\xDE\xAD"

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_file_header("no_existe.txt", 10)

def test_not_a_file(tmp_path):
    # Crea un directorio
    dir_path = tmp_path / "folder"
    dir_path.mkdir()
    
    with pytest.raises(ValueError):
        read_file_header(str(dir_path))
