import shutil
import subprocess
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOCALE_DIR = BASE_DIR / "locale"
POT_FILE = LOCALE_DIR / "messages.pot"
PO_FILE = LOCALE_DIR / "es" / "LC_MESSAGES" / "messages.po"
MO_FILE = LOCALE_DIR / "es" / "LC_MESSAGES" / "messages.mo"
TEMP_FILE_LIST = BASE_DIR / "files.txt"
BACKUP_FILE = PO_FILE.with_name(f"messages.po.bak")

def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"❌ Error al ejecutar: {' '.join(cmd)}")
        print(result.stderr)
    return result

def extract_translations():
    print("📦 Extrayendo cadenas del código fuente...")

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

    if POT_FILE.exists():
        print(f"✅ Plantilla POT generada: {POT_FILE.name}")

    if TEMP_FILE_LIST.exists():
        TEMP_FILE_LIST.unlink()
        print("🧹 Eliminado archivo temporal files.txt")

def backup_po_file():
    if PO_FILE.exists():
        shutil.copy(PO_FILE, BACKUP_FILE)
        print(f"💾 Backup creado: {BACKUP_FILE.name}")

def init_po_file():
    if not PO_FILE.exists():
        print("⚠️ No se encontró es.po, creando uno nuevo...")
        PO_FILE.parent.mkdir(parents=True, exist_ok=True)
        run([
            "msginit", "--no-translator", "--locale=es",
            "--input", str(POT_FILE), "--output-file", str(PO_FILE)
        ])

def show_duplicates(po_path: Path):
    lines = po_path.read_text(encoding="utf-8").splitlines()
    msgid_lines = [line for line in lines if line.startswith("msgid ")]
    seen = set()
    duplicates = set()

    for line in msgid_lines:
        if line in seen:
            duplicates.add(line)
        seen.add(line)

    if duplicates:
        print("⚠️  Duplicados detectados:")
        for d in sorted(duplicates):
            print(f"   {d}")
    return bool(duplicates)

def deduplicate_po():
    print("🧽 Eliminando duplicados en es.po...")
    if show_duplicates(PO_FILE):
        run(["msguniq", "--force-po", "--output", str(PO_FILE), str(PO_FILE)])
        print("✅ Duplicados eliminados.")
    else:
        print("✅ No se encontraron duplicados.")

def merge_translations():
    print("🔄 Fusionando mensajes nuevos con es.po...")
    run([
        "msgmerge", "--update", "--backup=none",
        str(PO_FILE), str(POT_FILE)
    ])

def verify_po():
    print("🧪 Verificando formato de es.po...")
    run(["msgfmt", "--check", str(PO_FILE)])

def compile_mo():
    print("📦 Compilando archivo MO...")
    run(["msgfmt", "-o", str(MO_FILE), str(PO_FILE)])
    if MO_FILE.exists():
        print(f"✅ Archivo compilado: {MO_FILE.name}")

def main():
    extract_translations()
    init_po_file()
    backup_po_file()
    deduplicate_po()       # Antes de merge
    merge_translations()
    deduplicate_po()       # Después de merge, por seguridad
    verify_po()
    compile_mo()

if __name__ == "__main__":
    main()
