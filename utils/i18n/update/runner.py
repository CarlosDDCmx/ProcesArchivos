"""
Runner para ejecutar la actualización de traducciones en múltiples idiomas.

Se puede importar como módulo o ejecutar directamente desde consola:
    python -m utils.i18n.update.runner --locales es en ja --dry-run
"""

import argparse
from .paths import POT_FILE, get_paths_for_lang
from .operations import (
    extract_translations,
    init_po_file,
    backup_po_file,
    deduplicate_po,
    merge_translations,
    verify_po,
    compile_mo,
    validate_po_language,
    fix_language_header,
    check_missing_translations,
)
from ..core import safe_print


def main(locales: list[str] = ["es"], dry_run: bool = False):
    """
    Ejecuta el flujo completo para cada idioma.

    Args:
        locales: Lista de códigos de idioma (ej: ["es", "en", "ja"]).
        dry_run: Si es True, muestra las acciones sin aplicarlas.
    """
    safe_print("🚀 Ejecutando flujo de actualización para idiomas:", "[i18n] Ejecutando runner")
    extract_translations()

    for lang in locales:
        paths = get_paths_for_lang(lang)
        po_path = paths["po"]
        mo_path = paths["mo"]

        if dry_run:
            safe_print(f"[dry-run] Procesando idioma '{lang}'", f"[i18n] Dry-run para {lang}")
        else:
            safe_print(f"🌍 Procesando idioma '{lang}'", f"[i18n] Procesando {lang}")

        # Crear archivo .po si no existe
        init_po_file(lang)

        # Crear respaldo
        if not dry_run:
            backup_po_file(po_path)

        # Eliminar duplicados
        if not dry_run:
            deduplicate_po(po_path)

        # Fusionar nuevas cadenas
        if not dry_run:
            merge_translations(po_path)

        # Eliminar duplicados nuevamente (por seguridad)
        if not dry_run:
            deduplicate_po(po_path)

        # Verificar formato del .po
        verify_po(po_path)

        # Compilar .mo (solo si no es dry-run)
        if not dry_run:
            compile_mo(po_path, mo_path)

        # Validar encabezado Language:
        validate_po_language(lang)

        # Corregir encabezado si está ausente
        if not dry_run:
            fix_language_header(lang)

        # Mostrar traducciones faltantes
        check_missing_translations(lang)


# ✅ Permitir ejecutar directamente como script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ejecuta el runner de traducciones")
    parser.add_argument("--locales", nargs="+", default=["es"], help="Idiomas a procesar (ej: es en ja)")
    parser.add_argument("--dry-run", action="store_true", help="Simula los pasos sin modificar archivos")

    args = parser.parse_args()
    main(locales=args.locales, dry_run=args.dry_run)
