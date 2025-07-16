import pytest
from ofimatic.loader_officezip import read_multiple_zip_entries
from zipfile import ZipFile
from pathlib import Path
import logging

# Carpeta temporal relativa para pruebas
TEMP_DIR = Path("tests/temp_files")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
def create_test_zip(path: Path, archivos: dict[str, bytes]):
    """Crea un archivo zip con contenido dado."""
    with ZipFile(path, "w") as zf:
        for nombre, contenido in archivos.items():
            zf.writestr(nombre, contenido)

# ─────────────────────────────────────────────────────────────────────────────
def test_read_multiple_zip_entries_ok():
    zip_path = TEMP_DIR / "test_ok.zip"
    contenido = {"a.txt": b"Hola", "b.txt": b"Mundo"}
    create_test_zip(zip_path, contenido)

    resultado = read_multiple_zip_entries(zip_path, ["a.txt", "b.txt"])
    assert resultado["a.txt"] == b"Hola"
    assert resultado["b.txt"] == b"Mundo"

# ─────────────────────────────────────────────────────────────────────────────
def test_read_multiple_zip_entries_ignore_missing():
    zip_path = TEMP_DIR / "test_parcial.zip"
    create_test_zip(zip_path, {"a.txt": b"Presente"})

    resultado = read_multiple_zip_entries(zip_path, ["a.txt", "b.txt"])
    assert "a.txt" in resultado
    assert "b.txt" not in resultado

# ─────────────────────────────────────────────────────────────────────────────
def test_read_multiple_zip_entries_bad_zip(caplog):
    caplog.set_level(logging.ERROR)
    zip_path = TEMP_DIR / "test_malo.zip"
    zip_path.write_bytes(b"No es un zip")

    with pytest.raises(RuntimeError) as exc:
        read_multiple_zip_entries(zip_path, ["algo.txt"])

    # Asegura que el mensaje generado coincida con lo esperado
    assert "archivo zip inválido" in str(exc.value).lower()

# ─────────────────────────────────────────────────────────────────────────────
def test_read_multiple_zip_entries_general_fail(caplog, monkeypatch):
    caplog.set_level(logging.ERROR)

    # Simula fallo al abrir el archivo
    monkeypatch.setattr("ofimatic.loader_officezip.ZipFile", lambda *_: (_ for _ in ()).throw(Exception("Fallo")))

    zip_path = TEMP_DIR / "test_error_general.zip"
    zip_path.write_bytes(b"Contenido falso")

    with pytest.raises(RuntimeError) as exc:
        read_multiple_zip_entries(zip_path, ["x.txt"])
    assert "fallo" in str(exc.value).lower()
