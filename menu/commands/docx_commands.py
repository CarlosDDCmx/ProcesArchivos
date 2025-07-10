from .base import Command
from utils.i18n.safe import safe_gettext as _
from memory import get_active_event
from ofimatic.loader_docx import read_docx, stats_docx, metadata_docx

class ReadDOCXCommand(Command):
    def execute(self, navigator):
        evt = get_active_event()
        if not evt:
            print(_("docx_no_activo"))
            return

        data = read_docx(evt.path)
        evt.metadata["docx_data"] = data

        paragraphs = data.get("paragraphs", [])
        print("\n".join(paragraphs[:10]) + (" …" if len(paragraphs) > 10 else ""))


class StatsDOCXCommand(Command):
    def execute(self, navigator):
        evt = get_active_event()
        if not evt:
            print(_("docx_no_activo"))
            return

        data = evt.metadata.get("docx_data")
        if not data:
            print(_("docx_no_datos"))
            return

        stats = stats_docx(data)
        evt.metadata["stats"] = stats

        print(_("docx_stats_titulo"))
        for key, value in stats.items():
            print(f"  {key}: {value}")


class MetadataDOCXCommand(Command):
    def execute(self, navigator):
        evt = get_active_event()
        if not evt:
            print(_("docx_no_activo"))
            return

        meta = metadata_docx(evt.path)
        evt.metadata["docx_meta"] = meta

        if not meta:
            print(_("docx_sin_metadata"))
            return

        print(_("docx_metadata_titulo"))
        for k, v in meta.items():
            print(f"  {k}: {v}")
