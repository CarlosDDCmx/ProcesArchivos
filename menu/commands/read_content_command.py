from .base import Command
from memory import get_active_event
from memory.events import DetectedFamily
from ofimatic import get_format_handler
from utils.i18n.safe import safe_gettext as _
import logging


class ReadContentCommand(Command):
    def execute(self, navigator):
        evt = get_active_event()
        if not evt:
            print(_("sin_archivo_activo"))
            return

        if evt.family not in {DetectedFamily.OPENDOCUMENT, DetectedFamily.OFFICE_ZIP}:
            print(_("tipo_no_soportado"))
            return

        path = evt.path
        try:
            handler = get_format_handler(evt.metadata.get("mime_type"))
            read_fn = handler["read"]
            content = read_fn(path)

            evt.metadata["content"] = content
            paragraphs = content.get("paragraphs") or []

            if not paragraphs:
                print(_("sin_parrafos"))
                return

            print("\n".join(paragraphs[:10]) + (" …" if len(paragraphs) > 10 else ""))
        except Exception as e:
            logging.error(_("error_lectura_contenido").format(error=str(e)))
            print(_("error_lectura_contenido").format(error=str(e)))
