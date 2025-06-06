import subprocess
import sys
import tempfile
from pathlib import Path

CLI_PATH = Path("cli/main.py")

def run_cli(args):
    return subprocess.run(
        [sys.executable, str(CLI_PATH)] + args,
        capture_output=True,
        text=True
    )

def test_detect_known_file(tmp_path):
    # Crea archivo con firma ZIP
    file = tmp_path / "sample.zip"
    file.write_bytes(b"PK\x03\x04" + b"\x00" * 60)

    result = run_cli([
        str(file),
        "--bytes", "64",
        "--log-level", "DEBUG",
        "--lang", "es"
    ])

    assert result.returncode == 0
    assert "ZIP" in result.stdout

def test_unknown_signature(tmp_path):
    file = tmp_path / "file.bin"
    file.write_bytes(b"\x00\x01\x02\x03" * 16)

    result = run_cli([
        str(file),
        "--lang", "en"
    ])

    assert result.returncode == 1
    assert "Unknown" in result.stdout

def test_error_file_not_found():
    result = run_cli(["no_file.xyz", "--lang", "en"])
    assert result.returncode == 2
    assert "does not exist" in result.stderr

def test_quiet_mode(tmp_path):
    file = tmp_path / "quiet.zip"
    file.write_bytes(b"PK\x03\x04" + b"\x00" * 60)

    result = run_cli([
        str(file),
        "--quiet",
        "--enable-logging"
    ])

    assert result.returncode == 0
    assert result.stdout.strip() == ""  # nada en salida estándar

def test_log_file_created(tmp_path):
    file = tmp_path / "to_log.zip"
    file.write_bytes(b"PK\x03\x04" + b"\x00" * 60)

    log_file = tmp_path / "log.txt"

    result = run_cli([
        str(file),
        "--enable-logging",
        "--log-file", str(log_file)
    ])

    assert result.returncode == 0
    assert log_file.exists()
    assert "ZIP" in log_file.read_text(encoding="utf-8")
