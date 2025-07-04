import argparse
import builtins
import logging
import os
import sys

from menu.navigator import Navigator
from menu.menus.main_menu import build_main_menu
from utils.i18n import get_translator
from utils.logger.core import configure_logger

def main() -> None:
    """Procesa los argumentos CLI y arranca la aplicación."""
    import memory.subscribers  # efectos colaterales de registro

    # ── Parseo de argumentos ───────────────────────────────────────────────
    parser = argparse.ArgumentParser(
        description="CLI tool for file analysis"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "-l", "--lang",
        type=str,
        help="Set language code (e.g. en, es, fr)"
    )
    parser.add_argument(
        "--log",
        action="store_true",
        help="Enable log file recording"
    )
    parser.add_argument(
        "--log-path",
        type=str,
        help="Custom path for saving logs"
    )
    parser.add_argument(
        "--debug-file",
        type=str,
        help="Detect file type and exit"
    )
    args = parser.parse_args()

    # ── Internacionalización ──────────────────────────────────────────────
    get_translator(args.lang)
    _ = builtins._

    # ── Configuración de logging ──────────────────────────────────────────
    configure_logger(
        verbose=args.verbose,
        log_to_file=args.log,
        log_path=args.log_path,
        rotate=True,          # rota el archivo cuando crece
        name=None             # logger raíz
    )

    # ── Aseguramos salida UTF‑8 coherente ─────────────────────────────────
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

    logging.debug(_("idioma_estab").format(lang=args.lang or "system default"))

    # ── Navegador de menús ────────────────────────────────────────────────
    navigator = Navigator()
    try:
        navigator.go_to(build_main_menu)
    except KeyboardInterrupt:
        logging.info(_("salir_linea"))
    except Exception:
        logging.exception(_("logger_error_inesp"))


if __name__ == "__main__":
    main()