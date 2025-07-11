from .base import Command
from memory import get_active_event
from ofimatic.loader_dispatch import get_format_handler
from utils.i18n.safe import safe_gettext as _
import logging


class MetadataCommand(Command):
    def execute(self, navigator):
        evt = get_active_event()
        if not evt:
            print(_("sin_archivo_activo"))
            return

        try:
            mime = evt.metadata.get("mime_type")
            path = evt.path

            handler = get_format_handler(mime)

            if "metadata" not in handler:
                print(_("error_no_soporta_metadatos"))
                return

            meta = handler["metadata"](path)
            evt.metadata["file_meta"] = meta

            print(_("metadatos_obtenidos"))
            for k, v in meta.items():
                print(f"{k}: {v}")

        except Exception as e:
            logging.error(_("error_lectura_metadatos").format(error=str(e)))
            print(_("error_lectura_metadatos").format(error=str(e)))
