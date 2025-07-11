from .base import Command
from memory import get_active_event
from ofimatic.loader_dispatch import get_format_handler
from utils.i18n.safe import safe_gettext as _
import logging

logger = logging.getLogger(__name__)

class ReadSpreadsheetCommand(Command):
    def execute(self, navigator):
        evt = get_active_event()
        if not evt or not evt.metadata:
            print(_("error_no_documento_activo"))
            return

        mime = evt.metadata.get("mime_type")
        try:
            handler = get_format_handler(mime)
        except ValueError as e:
            print(str(e))
            return

        read_fn = handler.get("read")
        if not read_fn:
            print(_("error_no_soporta_lectura"))
            return

        try:
            data = read_fn(evt.path)
            evt.metadata["opendoc_data"] = data
            print(_("ods_leido").format(sheets=len(data.get("sheets", {}))))
        except Exception as exc:
            print(_("ods_error").format(error=str(exc)))
            logger.error("❌ Error leyendo ODS: %s", str(exc))

class MetadataSpreadsheetCommand(Command):
    def execute(self, navigator):
        evt = get_active_event()
        if not evt or not evt.metadata:
            print(_("error_no_documento_activo"))
            return

        mime = evt.metadata.get("mime_type")
        try:
            handler = get_format_handler(mime)
        except ValueError as e:
            print(str(e))
            return

        meta_fn = handler.get("meta")
        if not meta_fn:
            print(_("error_no_soporta_metadatos"))
            return

        try:
            meta = meta_fn(evt.path)
            evt.metadata["opendoc_meta"] = meta
            print(_("ods_meta_ok"))
            for k, v in meta.items():
                print(f"• {k}: {v}")
        except Exception as exc:
            print(_("ods_error").format(error=str(exc)))
            logger.error("❌ Error metadatos ODS: %s", str(exc))
