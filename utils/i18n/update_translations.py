import argparse
import os
import sys
import tempfile

from utils.i18n.update.paths import get_paths_for_lang
from utils.i18n.update.operations import (
    extract_translations,
    init_po_file,
    backup_po_file,
    deduplicate_po,
    merge_translations,
    verify_po,
    compile_mo,
    list_locales,
    validate_po_language,
    check_missing_translations,
    fix_language_header,
    force_utf8_encoding,
    prepare_log_file,
    append_log,
)

def running_in_test_or_tmp():
    """Detecta si el script corre en pytest o carpeta temporal."""
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True
    cwd = os.getcwd()
    temp_dirs = [tempfile.gettempdir(), "/tmp", "\\tmp"]
    return any(cwd.startswith(td) for td in temp_dirs)

def main():
    parser = argparse.ArgumentParser(
        description="🛠 Herramienta para gestionar traducciones (.po/.mo)"
    )
    parser.add_argument("--extract", action="store_true", help="Extrae cadenas de texto a un archivo .pot")
    parser.add_argument("--init", action="store_true", help="Inicializa el archivo <locale>.po si no existe")
    parser.add_argument("--backup", action="store_true", help="Crea un respaldo del archivo <locale>.po")
    parser.add_argument("--dedup", action="store_true", help="Elimina cadenas duplicadas del archivo <locale>.po")
    parser.add_argument("--merge", action="store_true", help="Fusiona nuevos mensajes con <locale>.po")
    parser.add_argument("--verify", action="store_true", help="Verifica el formato del archivo <locale>.po")
    parser.add_argument("--compile", action="store_true", help="Compila el archivo <locale>.mo")
    parser.add_argument("--all", action="store_true", help="Ejecuta el flujo completo")
    parser.add_argument("--list", action="store_true", help="Muestra los idiomas disponibles")
    parser.add_argument("--locales", nargs="+", default=["es"], help="Lista de idiomas a procesar (ej: es en fr ja)")
    parser.add_argument("--check-missing", action="store_true", help="Verifica cadenas sin traducir (msgstr vacío)")
    parser.add_argument("--fix-lang-header", action="store_true", help="Corrige el encabezado 'Language:' del archivo .po")
    parser.add_argument("--log", action="store_true", help="Guarda los resultados en logs/i18n_report.log (sobrescribe)")

    args = parser.parse_args()

    if args.log:
        prepare_log_file()

    if args.list:
        list_locales()
        sys.exit(0)

    if args.extract or args.all:
        extract_translations()
        if args.log:
            append_log("📦 Extracción de cadenas completada")

    summary = []

    for lang in args.locales:
        paths = get_paths_for_lang(lang)
        po_path = paths["po"]
        mo_path = paths["mo"]
        steps = []

        if args.init or args.all:
            init_po_file(lang)
            steps.append("init")
            if args.log: append_log(f"[{lang}] .po creado")

        if args.backup or args.all:
            backup_po_file(po_path)
            steps.append("backup")
            if args.log: append_log(f"[{lang}] Backup generado")

        if args.dedup or args.all:
            deduplicate_po(po_path)
            steps.append("dedup")
            if args.log: append_log(f"[{lang}] Duplicados limpiados")

        if args.merge or args.all:
            merge_translations(po_path)
            steps.append("merge")
            if args.log: append_log(f"[{lang}] Cadenas fusionadas")

        if args.dedup or args.all:
            deduplicate_po(po_path)

        if args.verify or args.all:
            verify_po(po_path)
            steps.append("verify")
            if args.log: append_log(f"[{lang}] Formato verificado")

        if args.compile or args.all:
            compile_mo(po_path, mo_path)
            steps.append("compile")
            if args.log: append_log(f"[{lang}] Archivo .mo generado")

        validate_po_language(lang)
        steps.append("validate")

        if args.check_missing or args.all:
            check_missing_translations(lang)
            steps.append("missing")
            if args.log: append_log(f"[{lang}] Cadenas sin traducir revisadas")

        if args.fix_lang_header or args.all:
            fix_language_header(lang)
            steps.append("fix_lang")
            if args.log: append_log(f"[{lang}] Encabezado 'Language:' corregido")

        force_utf8_encoding(po_path)
        steps.append("utf8")
        if args.log: append_log(f"[{lang}] Codificación forzada a UTF-8")

        summary.append((lang, steps))

        if args.log:
            append_log("\n📝 Resumen final:")
            append_log(f"Total de idiomas procesados: {len(summary)}")
            for lang, steps in summary:
                append_log(f"  • {lang}: {' → '.join(steps)}")

            from utils.i18n.update.operations import finalize_log
            finalize_log()

if __name__ == "__main__":
    main()
    
    
