import argparse
import logging
import builtins
from menu.navigator import Navigator
from menu.menus.main_menu import build_main_menu
from utils.logger import configure_logger
from utils.i18n import get_translator

def main():
    parser = argparse.ArgumentParser(description="CLI tool for file analysis")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-l", "--lang", type=str, help="Set language code (e.g. en, es, fr)")
    parser.add_argument("--log", action="store_true", help="Enable log file recording")
    parser.add_argument("--log-path", type=str, help="Custom path for saving logs")
    parser.add_argument("--debug-file", type=str, help="Detect file type and exit")

    args = parser.parse_args()

    # Inicializa traducción global antes de usar builtins._
    get_translator(args.lang)
    _ = builtins._

    configure_logger(
        verbose=args.verbose,
        log_to_file=args.log,
        log_path=args.log_path,
        lang_code=args.lang or "es"
    )

    logging.debug(_("idioma_estab").format(lang=args.lang or "system default"))

    navigator = Navigator()
    try:
        navigator.go_to(build_main_menu)
    except KeyboardInterrupt:
        logging.info(_("salir_linea"))
    except Exception:
        logging.exception(_("logger_error_inesp"))

if __name__ == "__main__":
    main()