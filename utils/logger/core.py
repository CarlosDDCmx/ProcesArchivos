import logging
import os, io
import faulthandler
from datetime import datetime
from logging.handlers import RotatingFileHandler
from utils.i18n.safe import safe_gettext as _


def configure_logger(
    *,
    verbose: bool = False,
    log_to_file: bool = False,
    log_path: str | os.PathLike | None = None,
    name: str | None = None,
    rotate: bool = False,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 3,
) -> logging.Logger:
    """
    Configura y devuelve un logger; si *name* es None actúa sobre el logger raíz.
    """
    # Nivel de verbosidad
    level = logging.DEBUG if verbose else logging.INFO
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitamos duplicar handlers al ser llamada varias veces
    if logger.handlers:
        return logger

    # ── Handler de consola ────────────────────────────────────────────────
    console_handler = logging.StreamHandler()
    handlers: list[logging.Handler] = [console_handler]

    # ── Handler de archivo ────────────────────────────────────────────────
    if log_to_file:
        try:
            log_dir = os.path.abspath(log_path or "logs")
            os.makedirs(log_dir, exist_ok=True)
            date_stamp = datetime.now().strftime("%Y%m%d")
            log_file = os.path.join(log_dir, f"log_{date_stamp}.log")

            if rotate:
                file_handler: logging.Handler = RotatingFileHandler(
                    log_file,
                    mode="a",
                    maxBytes=max_bytes,
                    backupCount=backup_count,
                    encoding="utf-8",
                )
            else:
                file_handler = logging.FileHandler(
                    log_file, mode="a", encoding="utf-8"
                )

            handlers.append(file_handler)
        except Exception as exc:
            # Mensaje traducido si falla la creación del directorio
            print(_("logger_error_crea_dir").format(error=str(exc)))
            log_to_file = False

    # ── Formato común para todos los handlers ─────────────────────────────
    log_format = (
        "%(asctime)s | %(levelname)-8s | %(threadName)s | %(module)s: %(message)s"
    )
    date_format = "%H:%M:%S"
    for handler in handlers:
        handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
        logger.addHandler(handler)

    # ── Mensajes iniciales ────────────────────────────────────────────────
    logger.info(_("inicio_app"))
    if verbose:
        logger.debug(_("verbose_hab"))
        try:
            faulthandler.enable()
        except (io.UnsupportedOperation, AttributeError):
            logger.debug("⚠️ faulthandler no disponible en este entorno")
    if log_to_file:
        logger.info(_("ruta_logs_msj").format(path=log_file))

    return logger
