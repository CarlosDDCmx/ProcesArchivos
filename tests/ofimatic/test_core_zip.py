import pytest
from pathlib import Path
from ofimatic.core_zip import read_zip_entry, read_multiple_zip_entries, InvalidZipFile
from zipfile import ZipFile
import os
from utils.i18n.safe import safe_gettext as _

TEMP_DIR = Path("tests/temp_files")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def create_test_zip(zip_path: Path, entries: dict):
    with ZipFile(zip_path, "w") as zf:
        for name, content in entries.items():
            zf.writestr(name, content)

# Prueba que se puede leer una entrada específica de un ZIP válido
def test_read_zip_entry_valid():
    zip_path = TEMP_DIR / "valido.zip"
    create_test_zip(zip_path, {"a.txt": b"contenido"})

    data = read_zip_entry(zip_path, "a.txt")
    assert data == b"contenido"

# Prueba que se lanza excepción si el archivo no es un ZIP
def test_read_zip_entry_invalid_zip():
    corrupt_path = TEMP_DIR / "corrupto.zip"
    corrupt_path.write_bytes(b"No es un zip")

    with pytest.raises(InvalidZipFile) as exc:
        read_zip_entry(corrupt_path, "archivo.txt")

    expected = _("loader_error").split("{")[0].strip()
    assert expected in str(exc.value)

# Prueba que se pueden leer múltiples entradas con 1 hilo
def test_read_multiple_entries_sequential():
    zip_path = TEMP_DIR / "multi1.zip"
    create_test_zip(zip_path, {"1.txt": b"A", "2.txt": b"B"})

    result = read_multiple_zip_entries(zip_path, ["1.txt", "2.txt"], workers=0)
    assert result["1.txt"] == b"A"
    assert result["2.txt"] == b"B"

# Prueba que se pueden leer múltiples entradas concurrentemente
def test_read_multiple_entries_concurrent():
    zip_path = TEMP_DIR / "multi2.zip"
    create_test_zip(zip_path, {"x.txt": b"X", "y.txt": b"Y"})

    result = read_multiple_zip_entries(zip_path, ["x.txt", "y.txt"], workers=2)
    assert result["x.txt"] == b"X"
    assert result["y.txt"] == b"Y"

# Prueba que una entrada inexistente lanza KeyError
def test_read_zip_entry_missing_file():
    zip_path = TEMP_DIR / "faltante.zip"
    create_test_zip(zip_path, {"a.txt": b"existe"})

    with pytest.raises(KeyError):
        read_zip_entry(zip_path, "no_existe.txt")