"""
Orquesta las operaciones en el orden correcto.
"""
from .operations import (
    extract_translations,
    init_po_file,
    backup_po_file,
    deduplicate_po,
    merge_translations,
    verify_po,
    compile_mo,
)

def main(dry_run: bool = False):
    """
    Ejecuta el flujo completo de actualización de archivos de traducción.
    Esta función orquesta la extracción, inicialización, depuración,
    fusión, verificación y compilación de traducciones.
    """
    extract_translations()
    init_po_file()
    backup_po_file()
    deduplicate_po()       # Antes de la fusión
    merge_translations()
    deduplicate_po()       # Después de la fusión, por seguridad
    verify_po()
    compile_mo()