from menu.menu import Menu
from menu.commands.submenu_command import SubMenuCommand
from menu.commands.concrete_command import BackCommand
from menu.menus.detectors_menu import build_detector_menu
from utils.i18n.safe import safe_gettext as _

def build_tools_menu():
    menu = Menu(title=_("herramientas"))
    menu.add_command("1", SubMenuCommand(_("detector"), build_detector_menu), _("detector"))
    menu.add_command("0", BackCommand(), _("volver"))
    return menu