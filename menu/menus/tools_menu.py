from menu.menu import Menu
from menu.commands.concrete_command import BackCommand
from menu.commands.submenu_command import SubMenuCommand
from menu.commands.detect_file_command import DetectFileCommand
from menu.commands.read_content_command import ReadODFCommand, ReadDOCXCommand
from menu.menus.docs_menu import build_docs_menu
from menu.menus.docx_menu import build_docx_menu
from memory import get_active_event
from memory.events import DetectedFamily
from utils.i18n.safe import safe_gettext as _


def build_tools_menu() -> Menu:
    menu = Menu(title=_("herramientas"))
    menu.add_command("1", DetectFileCommand(), _("detector")) # Opción 1: detector de tipo de archivo

    active = get_active_event()
    # Numeración dinámica para las opciones “leer contenido”
    next_idx = 2

    if active and active.family is DetectedFamily.OPENDOCUMENT:
        menu.add_command(
            str(next_idx),
            SubMenuCommand(_("procesar_opendoc"), build_docs_menu),
            _("procesar_opendoc"),
        )
        next_idx += 1

    if active and active.family is DetectedFamily.OFFICE_ZIP:
        menu.add_command(
            str(next_idx), 
            SubMenuCommand(_("procesar_docx"), build_docx_menu), 
            _("procesar_docx"))
        next_idx += 1

    # Opción 0: volver
    menu.add_command("0", BackCommand(), _("volver"))
    return menu