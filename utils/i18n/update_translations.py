import argparse
import sys
import os
import tempfile
from utils.i18n.update import (
    extract_translations,
    init_po_file,
    backup_po_file,
    deduplicate_po,
    merge_translations,
    verify_po,
    compile_mo,
)

def running_in_test_or_tmp():
    """
    Detecta si el script corre dentro de pytest o en una carpeta temporal.
    """
    # 1. Modo pytest detectado
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True

    # 2. CWD dentro de un directorio temporal
    cwd = os.getcwd()
    temp_dirs = [tempfile.gettempdir(), "/tmp", "\\tmp"]
    return any(cwd.startswith(td) for td in temp_dirs)

def main():
    parser = argparse.ArgumentParser(
        description="🛠 Herramienta para gestionar traducciones (.po/.mo)"
    )
    parser.add_argument(
        "--extract", action="store_true", help="Extrae cadenas de texto a un archivo .pot"
    )
    parser.add_argument(
        "--init", action="store_true", help="Inicializa el archivo <locale>.po si no existe"
    )
    parser.add_argument(
        "--backup", action="store_true", help="Crea un respaldo del archivo <locale>.po"
    )
    parser.add_argument(
        "--dedup", action="store_true", help="Elimina cadenas duplicadas del archivo <locale>.po"
    )
    parser.add_argument(
        "--merge", action="store_true", help="Fusiona nuevos mensajes con <locale>.po"
    )
    parser.add_argument(
        "--verify", action="store_true", help="Verifica el formato del archivo <locale>.po"
    )
    parser.add_argument(
        "--compile", action="store_true", help="Compila el archivo <locale>.mo"
    )
    parser.add_argument(
        "--all", action="store_true", help="Ejecuta el flujo completo"
    )
    parser.add_argument(
        "--locale", default="es", help="Código de idioma (por defecto: 'es')"
    )

    args = parser.parse_args()
    lang = args.locale

    if args.all:
        extract_translations()
        init_po_file(lang)
        backup_po_file(lang)
        deduplicate_po(lang)
        merge_translations(lang)
        deduplicate_po(lang)
        verify_po(lang)
        compile_mo(lang)
    else:
        if args.extract:
            extract_translations()
        if args.init:
            init_po_file(lang)
        if args.backup:
            backup_po_file(lang)
        if args.dedup:
            deduplicate_po(lang)
        if args.merge:
            merge_translations(lang)
        if args.verify:
            verify_po(lang)
        if args.compile:
            compile_mo(lang)

if __name__ == "__main__":
    main()
