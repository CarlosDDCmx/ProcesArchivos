import argparse
import sys
from core.reader import read_file_header
from core.detector import load_signatures, detect_from_header
from core.logger import LoggerManager
from core.i18n import load_language, t

def main():
    # Primer paso: detectar idioma antes de mostrar mensajes
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--lang", default=None)
    pre_args, _ = pre_parser.parse_known_args()
    load_language(pre_args.lang)

    parser = argparse.ArgumentParser(description=t("help_text"))
    parser.add_argument("archivo", help=t("file_argument"))
    parser.add_argument("--bytes", type=int, default=64, help=t("bytes_argument"))
    parser.add_argument("--log-level", default="INFO", help=t("log_level_argument"))
    parser.add_argument("--quiet", action="store_true", help=t("quiet_argument"))
    parser.add_argument("--enable-logging", action="store_true", help=t("log_argument"))
    parser.add_argument("--lang", default=None, help=t("lang_argument"))
    parser.add_argument("--log-file", help=t("log_file"))
    args = parser.parse_args()

    # Se vuelve a cargar el idioma final si cambió
    load_language(args.lang)

    logger = LoggerManager.get_logger(
        log_file=args.log_file,
        log_level=args.log_level,
        enable_logging=args.enable_logging
    )
    log_path = LoggerManager.get_log_path()

    try:
        header = read_file_header(args.archivo, args.bytes)
        firmas = load_signatures()
        tipo = detect_from_header(header, args.archivo, firmas)

        resultado = tipo or t("unknown")
        logger.info(t("file_detected", tipo=resultado))

        logger.debug(t("main.summary_scan", archivo=args.archivo, bytes_leidos=args.bytes, resultado=resultado))
        if args.enable_logging and log_path:
            logger.debug(f"{t("main.log_path", log_path)}")

        if not args.quiet:
            print(f"\n{t('result', tipo=resultado)}")
            if args.enable_logging and log_path:
                print(t("log_saved", archivo=str(log_path)))

        sys.exit(0 if tipo else 1)

    except Exception as e:
        logger.error(t("error_processing", error=str(e)))
        if not args.quiet:
            print("❌ " + t("error_processing", error=str(e)))
            if args.enable_logging and log_path:
                print(t("log_saved", ruta=str(log_path)))
        sys.exit(2)

if __name__ == "__main__":
    main()
