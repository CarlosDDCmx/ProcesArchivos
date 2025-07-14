import subprocess, sys
from pathlib import Path
import pytest

# ────────────────────────────────────────────────────────────────────────────────
# 🧪 UTILIDADES PARA BACKUP Y RESTAURACIÓN SEGURA
# ────────────────────────────────────────────────────────────────────────────────

def safe_backup(path: Path):
    backup = path.with_suffix(".bak")
    if backup.exists():
        backup.unlink()
    if path.exists():
        path.rename(backup)
    return backup

def safe_restore(original: Path, backup: Path):
    if original.exists():
        original.unlink()
    if backup.exists():
        backup.rename(original)

# ────────────────────────────────────────────────────────────────────────────────
# ✅ PRUEBA DE INTEGRACIÓN GENERAL (EJECUCIÓN CORRECTA)
# ────────────────────────────────────────────────────────────────────────────────

def test_update_translations_script_runs():
    """✅ Ejecuta el subpaquete update como script con -m (flujo completo)"""
    result = subprocess.run(
        ["python", "-m", "utils.i18n.update"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, result.stderr
    assert "📦" in result.stdout or "✅" in result.stdout or "⚠️" in result.stdout, result.stdout


# ────────────────────────────────────────────────────────────────────────────────
# ❌ CASO: FALTA EL ARCHIVO .po
# ────────────────────────────────────────────────────────────────────────────────

def test_fail_if_no_po():
    """❌ Falla si el archivo .po no existe"""
    po_path = Path("locale/es/LC_MESSAGES/messages.po").resolve()
    backup = safe_backup(po_path)

    try:
        result = subprocess.run(
            ["python", "-m", "utils.i18n.update"],
            capture_output=True,
            text=True
        )

        assert result.returncode != 0, "El script debería fallar si falta messages.po"
        assert "po" in result.stderr.lower() or "error" in result.stderr.lower()
    finally:
        safe_restore(po_path, backup)


# ────────────────────────────────────────────────────────────────────────────────
# ❌ CASO: ARCHIVO .po INVÁLIDO (UTF-8 O ESTRUCTURA)
# ────────────────────────────────────────────────────────────────────────────────

def test_fail_if_invalid_po():
    """❌ Falla si el archivo .po contiene errores de sintaxis o codificación inválida"""
    po_path = Path("locale/es/LC_MESSAGES/messages.po").resolve()
    backup = safe_backup(po_path)

    try:
        # Archivo con bytes no válidos (no UTF-8)
        po_path.write_bytes(b'\xff\xfe\x00INVALID PO FILE')

        result = subprocess.run(
            ["python", "-m", "utils.i18n.update"],
            capture_output=True,
            text=True,
            errors="replace"
        )

        assert result.returncode != 0, "El script debería fallar con archivo .po inválido"
        assert "error" in result.stderr.lower() or "decode" in result.stderr.lower()
    finally:
        safe_restore(po_path, backup)


# ────────────────────────────────────────────────────────────────────────────────
# ❌ CASO: ARCHIVO .pot MALFORMADO
# ────────────────────────────────────────────────────────────────────────────────

def test_fail_if_bad_po(isolated_locale):
    # Estamos dentro de tmp_path, por lo que los archivos reales no se tocan
    pot_path = Path("messages.pot")
    pot_path.write_text("contenido inválido", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "utils.i18n.update"],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0 or "error" in result.stderr.lower(), (
        "El script debería fallar con .pot inválido o al menos mostrar un error.\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
