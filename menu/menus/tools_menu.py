from menu.menu import Menu
from menu.commands.concrete_command import BackCommand
from menu.commands.detect_file_command import DetectFileCommand
from menu.commands.read_content_command import ReadContentCommand
from menu.commands.stats_command import StatsCommand
from menu.commands.metadata_command import MetadataCommand
from memory import get_active_event
from ofimatic.loader_dispatch import SUPPORTED_FORMATS
from utils.i18n.safe import safe_gettext as _


def build_tools_menu() -> Menu:
    menu = Menu(title=_("herramientas"))

    menu.add_command("1", DetectFileCommand(), _("detector"))  # Opción 1
    next_idx = 2

    active = get_active_event()
    if active:
        mime = active.metadata.get("mime_type")
        handler = SUPPORTED_FORMATS.get(mime)
        if handler:
            doc_type = handler.get("type")

            # Se asume que todos los documentos usan el mismo ReadContentCommand
            menu.add_command(str(next_idx), ReadContentCommand(), _("leer_contenido"))
            next_idx += 1

            # Si soporta estadísticas
            if handler.get("stats"):
                menu.add_command(str(next_idx), StatsCommand(), _("obtener_estadisticas"))
                next_idx += 1

            # Si soporta metadatos
            if handler.get("metadata"):
                menu.add_command(str(next_idx), MetadataCommand(), _("obtener_metadatos"))
                next_idx += 1

            # Espacio para pptx, xlsx, etc.

    menu.add_command("0", BackCommand(), _("volver"))
    return menu
