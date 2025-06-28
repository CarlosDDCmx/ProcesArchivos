from menu.menu import Menu
from menu.commands.submenu_command import SubMenuCommand  # si usas sub‑menús anidados
from menu.commands.concrete_command import BackCommand
from menu.commands.detect_file_command import DetectFileCommand
from menu.commands.read_content_command import ReadODFCommand, ReadDOCXCommand
from memory.subscribers import family_exists
from memory.events import DetectedFamily
from utils.i18n.safe import safe_gettext as _


def build_tools_menu() -> Menu:
    """Construye el sub‑menú Herramientas."""
    menu = Menu(title=_("herramientas"))

    # Opción 1: detector de tipo de archivo
    menu.add_command("1", DetectFileCommand(), _("detector"))

    # Numeración dinámica para las opciones “leer contenido”
    next_index = 2

    if family_exists(DetectedFamily.OPENDOCUMENT):
        menu.add_command(str(next_index), ReadODFCommand(), _("leer_contenido_odf"))
        next_index += 1

    if family_exists(DetectedFamily.OFFICE_ZIP):
        menu.add_command(str(next_index), ReadDOCXCommand(), _("leer_contenido_docx"))
        next_index += 1

    # Opción 0: volver
    menu.add_command("0", BackCommand(), _("volver"))

    return menu