import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from .commands import run
from ..core import safe_print
from .paths import BASE_DIR, POT_FILE, TEMP_FILE_LIST, LOCALE_DIR, get_paths_for_lang

LOG_FILE = Path("logs/i18n_report.log")
START_TIME = datetime.now()

def extract_translations():
    """Extrae las cadenas traducibles del proyecto usando rutas relativas."""
    safe_print("📦 Extrayendo cadenas del código fuente...", "[i18n] Extrayendo cadenas del código fuente...")

    py_files = [
        str(f.relative_to(BASE_DIR))
        for f in BASE_DIR.rglob("*.py")
        if "venv" not in str(f)
    ]

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

    result = subprocess.run(["msgfmt", "--check", str(POT_FILE)], capture_output=True, text=True)
    if result.returncode != 0:
        safe_print("❌ El archivo .pot tiene errores de formato.", "[i18n] Error en archivo .pot")
        print(result.stderr)
        exit(1)

    safe_print(f"✅ Plantilla POT generada: {POT_FILE.name}", f"[i18n] Plantilla POT generada: {POT_FILE.name}")

def backup_po_file(po_path: Path):
    """Crea respaldo del archivo .po, con timestamp si ya existe."""
    if not po_path.exists():
        return

    backup_path = po_path.with_suffix(".po.bak")

    if backup_path.exists():
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = po_path.with_name(f"{po_path.stem}_{timestamp}.po.bak")

    shutil.copy(po_path, backup_path)
    safe_print(f"💾 Backup creado: {backup_path.name}", f"[i18n] Backup creado: {backup_path.name}")

def init_po_file(lang: str):
    """Inicializa un archivo .po para el idioma si no existe y fuerza UTF-8."""
    paths = get_paths_for_lang(lang)
    po_path = paths["po"]
    pot_path = POT_FILE

    if not po_path.exists():
        safe_print(f"⚠️ No se encontró {lang}.po, creando uno nuevo...", f"[i18n] No se encontró {lang}.po, creando uno nuevo...")
        paths["dir"].mkdir(parents=True, exist_ok=True)

        run([
            "msginit", "--no-translator", "--locale", lang,
            "--input", str(pot_path), "--output-file", str(po_path)
        ])

        # 🔧 Postprocesar para garantizar UTF-8 en Content-Type
        try:
            content = po_path.read_text(encoding="utf-8", errors="replace")
            if "charset=" in content and "charset=UTF-8" not in content:
                lines = [
                    line.replace("charset=ISO-8859-1", "charset=UTF-8")
                        .replace("charset=CP1252", "charset=UTF-8")
                        .replace("charset=latin1", "charset=UTF-8")
                    for line in content.splitlines()
                ]
                po_path.write_text("\n".join(lines), encoding="utf-8")
                safe_print(f"🔧 Codificación forzada a UTF-8 para {lang}.po", f"[i18n] Charset corregido en {lang}.po")
        except Exception as e:
            safe_print(f"❌ Error al postprocesar {lang}.po: {e}", f"[i18n] Fallo en charset de {lang}.po")

def show_duplicates(po_path: Path):
    """Detecta líneas duplicadas en el archivo .po."""
    lines = po_path.read_text(encoding="utf-8", errors="replace").splitlines()
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

def deduplicate_po(po_path: Path):
    """Elimina entradas duplicadas del archivo .po."""
    safe_print(f"🧽 Eliminando duplicados en {po_path.name}...", f"[i18n] Eliminando duplicados en {po_path.name}...")
    if show_duplicates(po_path):
        run(["msguniq", "--force-po", "--output", str(po_path), str(po_path)])
        safe_print("✅ Duplicados eliminados.", "[i18n] Duplicados eliminados.")
    else:
        safe_print("✅ No se encontraron duplicados.", "[i18n] No se encontraron duplicados.")

def merge_translations(po_path: Path):
    """Fusiona nuevas cadenas del .pot en el .po."""
    safe_print(f"🔄 Fusionando mensajes nuevos con {po_path.name}...", f"[i18n] Fusionando mensajes nuevos con {po_path.name}...")
    run(["msgmerge", "--update", "--backup=none", str(po_path), str(POT_FILE)])

def verify_po(po_path: Path):
    """Verifica que el .po tenga formato válido."""
    safe_print(f"🧪 Verificando formato de {po_path.name}...", f"[i18n] Verificando formato de {po_path.name}...")
    run(["msgfmt", "--check", str(po_path)])

def compile_mo(po_path: Path, mo_path: Path):
    """Compila el archivo .mo desde el .po."""
    safe_print(f"📦 Compilando archivo MO para {po_path.name}...", f"[i18n] Compilando archivo MO para {po_path.name}...")
    fallback_path = BASE_DIR / "messages.mo"
    run(["msgfmt", "-o", str(mo_path), str(po_path)])
    if fallback_path.exists():
        fallback_path.unlink()

    if mo_path.exists():
        safe_print(f"✅ Archivo compilado: {mo_path.name}", f"[i18n] Archivo compilado: {mo_path.name}")

def list_locales():
    """Muestra los idiomas disponibles en locale/."""
    safe_print("🌍 Idiomas disponibles:", "[i18n] Idiomas disponibles:")
    if not LOCALE_DIR.exists():
        print("   (no hay traducciones aún)")
        return

    for lang_dir in sorted(LOCALE_DIR.iterdir()):
        if (lang_dir / "LC_MESSAGES" / "messages.po").exists():
            print(f"   {lang_dir.name}")

def validate_po_language(lang: str):
    """Verifica que el campo 'Language:' en el .po esté definido correctamente."""
    po_path = get_paths_for_lang(lang)["po"]
    if not po_path.exists():
        return

    content = po_path.read_text(encoding="utf-8", errors="replace")
    if f'Language: {lang}' not in content:
        safe_print(
            f"⚠️ El archivo {lang}.po no tiene definido 'Language: {lang}'",
            f"[i18n] Campo 'Language:' ausente o incorrecto en {lang}.po"
        )

def check_missing_translations(lang: str):
    """Muestra las cadenas sin traducir en el archivo .po (msgstr vacío)."""
    po_path = get_paths_for_lang(lang)["po"]
    if not po_path.exists():
        safe_print(f"❌ No se encontró el archivo .po para '{lang}'", f"[i18n] No existe {lang}.po")
        return

    lines = po_path.read_text(encoding="utf-8", errors="replace").splitlines()
    current_msgid = None
    missing = []

    for line in lines:
        if line.startswith("msgid "):
            current_msgid = line
        elif line.startswith("msgstr \"\"") and current_msgid:
            missing.append(current_msgid)
            current_msgid = None

    if missing:
        safe_print(f"❗ Traducciones faltantes en '{lang}':", f"[i18n] Traducciones faltantes en {lang}:")
        append_log(f"\n❗ Traducciones faltantes en '{lang}':")
        for m in missing:
            print(f"   {m}")
            append_log(f"   {m}")
    else:
        safe_print(f"✅ Todas las cadenas están traducidas en '{lang}'", f"[i18n] Todas las cadenas traducidas en {lang}")
        append_log(f"✅ Todas las cadenas están traducidas en '{lang}'")

def fix_language_header(lang: str):
    """Corrige el campo 'Language: <lang>' en el encabezado del archivo .po."""
    po_path = get_paths_for_lang(lang)["po"]
    if not po_path.exists():
        return

    content = po_path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    new_lines = []
    header_updated = False

    for line in lines:
        if line.startswith("Language: "):
            new_lines.append(f"\"Language: {lang}\\n\"")
            header_updated = True
        else:
            new_lines.append(line)

    if not header_updated:
        for i, line in enumerate(new_lines):
            if line.strip() == "":
                new_lines.insert(i, f"\"Language: {lang}\\n\"")
                break

    po_path.write_text("\n".join(new_lines), encoding="utf-8")
    safe_print(f"✏️ Encabezado actualizado: Language: {lang}", f"[i18n] Encabezado 'Language:' actualizado a {lang}")

def prepare_log_file():
    """Sobrescribe el archivo de log al comenzar el script."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text(f"# 📋 Reporte de traducción iniciado: {START_TIME.strftime('%Y-%m-%d %H:%M:%S')}\n", encoding="utf-8")

def append_log(line: str):
    """Agrega una línea al archivo de log."""
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{line}\n")

def finalize_log():
    """Agrega la hora final y duración del proceso al log."""
    end_time = datetime.now()
    duration = end_time - START_TIME
    append_log("\n# 🏁 Proceso completado:")
    append_log(f"# Hora final: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    append_log(f"# Duración total: {str(duration)}")

def force_utf8_encoding(po_path: Path):
    """
    Asegura que el archivo .po tenga codificación UTF-8 explícita.
    Corrige encabezado 'charset=...' y guarda el contenido como UTF-8.
    """
    if not po_path.exists():
        return

    try:
        content = po_path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        updated_lines = []
        changed = False

        for line in lines:
            if "charset=" in line:
                updated_line = line.replace("charset=CHARSET", "charset=UTF-8").replace("charset=ISO-8859-1", "charset=UTF-8")
                if updated_line != line:
                    changed = True
                updated_lines.append(updated_line)
            else:
                updated_lines.append(line)

        if changed:
            po_path.write_text("\n".join(updated_lines), encoding="utf-8")
            safe_print(f"✏️ Codificación actualizada a UTF-8 en {po_path.name}", f"[i18n] Codificación corregida en {po_path.name}")
    except Exception as e:
        safe_print(f"❌ Error corrigiendo codificación en {po_path.name}: {e}", f"[i18n] Error codificación en {po_path.name}")
