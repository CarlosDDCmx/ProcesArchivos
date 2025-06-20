import logging
import os
import faulthandler
from datetime import datetime
from utils.i18n.safe import safe_gettext as _

def configure_logger(verbose=False, log_to_file=False, log_path=None, lang_code="es"):

    level = logging.DEBUG if verbose else logging.INFO
    log_handlers = [logging.StreamHandler()]

    if log_to_file:
        try:
            log_dir = os.path.abspath(log_path or "logs")
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"log_{timestamp}.log")
            log_handlers.append(logging.FileHandler(log_file, mode="w", encoding="utf-8"))
        except Exception as err:
            print(_("logger_error_crea_dir").format(error=str(err)))
            log_to_file = False

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        handlers=log_handlers
    )

    logging.info(_("inicio_app"))
    if verbose:
        logging.debug(_("verbose_hab"))
        faulthandler.enable()
    if log_to_file:
        logging.info(_("ruta_logs_msj").format(path=log_file))
