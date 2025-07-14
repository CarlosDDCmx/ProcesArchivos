"""
Define operaciones individuales como extracción, backup, deduplicación, etc.
"""
import shutil
import subprocess
from pathlib import Path
from .commands import run
from ..core import safe_print
from utils.i18n.update.paths import BASE_DIR, POT_FILE, PO_FILE, MO_FILE, TEMP_FILE_LIST, BACKUP_FILE

def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        safe_print(f"❌ Error al ejecutar: {' '.join(cmd)}", f"[i18n] Error al ejecutar: {' '.join(cmd)}")
        print(result.stderr)
        # 🚨 TERMINAR EL SCRIPT si falla
        exit(1)
    return result

def extract_translations():
    """Extrae las cadenas traducibles del proyecto."""
    safe_print("📦 Extrayendo cadenas del código fuente...", "[i18n] Extrayendo cadenas del código fuente...")

    py_files = [str(f) for f in BASE_DIR.rglob("*.py") if "venv" not in str(f)]
    TEMP_FILE_LIST.write_text("\n".join(py_files), encoding="utf-8")

    run([
        "xgettext",
        "--language=Python",
        "--from-code=UTF-8",
        "--add-comments",
        "--output", str(POT_FILE),
        "--files-from", str(TEMP_FILE_LIST)
    ])

    if not POT_FILE.exists():
        safe_print("❌ No se generó el archivo .pot", "[i18n] No se generó el archivo .pot")
        exit(1)

    # 🧪 Validar el formato del archivo POT con msgfmt
    result = subprocess.run(["msgfmt", "--check", str(POT_FILE)], capture_output=True, text=True)
    if result.returncode != 0:
        safe_print("❌ El archivo .pot tiene errores de formato.", "[i18n] Error en archivo .pot")
        print(result.stderr)
        exit(1)

    safe_print(f"✅ Plantilla POT generada: {POT_FILE.name}", f"[i18n] Plantilla POT generada: {POT_FILE.name}")

def backup_po_file():
    """Crea una copia de seguridad del archivo .po si existe."""
    if PO_FILE.exists():
        shutil.copy(PO_FILE, BACKUP_FILE)
        safe_print(f"💾 Backup creado: {BACKUP_FILE.name}", f"[i18n] Backup creado: {BACKUP_FILE.name}")

def init_po_file():
    """Inicializa un archivo .po si no existe."""
    if not PO_FILE.exists():
        safe_print("⚠️ No se encontró es.po, creando uno nuevo...", "[i18n] No se encontró es.po, creando uno nuevo...")
        PO_FILE.parent.mkdir(parents=True, exist_ok=True)
        run([
            "msginit", "--no-translator", "--locale=es",
            "--input", str(POT_FILE), "--output-file", str(PO_FILE)
        ])

def show_duplicates(po_path: Path):
    """Detecta líneas duplicadas de msgid en el archivo .po."""
    lines = po_path.read_text(encoding="utf-8").splitlines()
    msgid_lines = [line for line in lines if line.startswith("msgid ")]
    seen = set()
    duplicates = set()

    for line in msgid_lines:
        if line in seen:
            duplicates.add(line)
        seen.add(line)

    if duplicates:
        safe_print("⚠️  Duplicados detectados:", "[i18n] Duplicados detectados:")
        for d in sorted(duplicates):
            print(f"   {d}")
    return bool(duplicates)

def deduplicate_po():
    """Elimina entradas duplicadas del archivo .po."""
    safe_print("🧽 Eliminando duplicados en es.po...", "[i18n] Eliminando duplicados en es.po...")
    if show_duplicates(PO_FILE):
        run(["msguniq", "--force-po", "--output", str(PO_FILE), str(PO_FILE)])
        safe_print("✅ Duplicados eliminados.", "[i18n] Duplicados eliminados.")
    else:
        safe_print("✅ No se encontraron duplicados.", "[i18n] No se encontraron duplicados.")

def merge_translations():
    """Fusiona mensajes nuevos del POT con el archivo PO."""
    safe_print("🔄 Fusionando mensajes nuevos con es.po...", "[i18n] Fusionando mensajes nuevos con es.po...")
    run([
        "msgmerge", "--update", "--backup=none",
        str(PO_FILE), str(POT_FILE)
    ])

def verify_po():
    """Verifica errores de formato en el archivo .po."""
    safe_print("🧪 Verificando formato de es.po...", "[i18n] Verificando formato de es.po...")
    run(["msgfmt", "--check", str(PO_FILE)])

def compile_mo():
    """Compila el archivo .mo desde el archivo .po."""
    safe_print("📦 Compilando archivo MO...", "[i18n] Compilando archivo MO...")
    run(["msgfmt", "-o", str(MO_FILE), str(PO_FILE)])
    if MO_FILE.exists():
        safe_print(f"✅ Archivo compilado: {MO_FILE.name}", f"[i18n] Archivo compilado: {MO_FILE.name}")