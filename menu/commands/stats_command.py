from .base import Command
from memory import get_active_event
from ofimatic.loader_dispatch import get_format_handler
from utils.i18n.safe import safe_gettext as _
import logging


class StatsCommand(Command):
    def execute(self, navigator):
        evt = get_active_event()
        if not evt:
            print(_("sin_archivo_activo"))
            return

        try:
            mime = evt.metadata.get("mime_type")
            content = evt.metadata.get("content")
            if not content:
                print(_("contenido_no_cargado"))
                return

            handler = get_format_handler(mime)
            stats = handler["stats"](content)

            evt.metadata["stats"] = stats
            print(_("stats_obtenidas"))
            for key, value in stats.items():
                print(f"{key}: {value}")
        except Exception as e:
            logging.error(_("error_lectura_stats").format(error=str(e)))
            print(_("error_lectura_stats").format(error=str(e)))
