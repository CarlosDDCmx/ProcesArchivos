from menu.menu import Menu
from menu.commands.concrete_command import BackCommand
from utils.i18n.safe import safe_gettext as _

# Placeholder
def build_pptx_menu() -> Menu:
    menu = Menu(title=_("menu_pptx"))
    # Futuro: comandos específicos para archivos PPTX

    # Opción 0: volver
    menu.add_command("0", BackCommand(), _("volver"))
    return menu
