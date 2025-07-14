"""
Punto de entrada del subpaquete 'update'.
Permite ejecutar el módulo con `python -m utils.i18n.update`.
"""

if __name__ == "__main__":
    from .runner import main
    from ..update_translations import running_in_test_or_tmp

    dry_run = running_in_test_or_tmp()
    main(dry_run=dry_run)