from menu.menu import Menu
from menu.commands.concrete_command import BackCommand
from menu.commands.docx_commands import (
    ReadDOCXCommand, 
    StatsDOCXCommand, 
    MetadataDOCXCommand)
from utils.i18n.safe import safe_gettext as _


def build_docx_menu() -> Menu:
    menu = Menu(title=_("menu_docx"))
    menu.add_command("1", ReadDOCXCommand(), _("leer_contenido"))
    menu.add_command("2", StatsDOCXCommand(), _("obtener_stats"))
    menu.add_command("3", MetadataDOCXCommand(), _("leer_metadatos"))
    menu.add_command("0", BackCommand(), _("volver"))
    return menu