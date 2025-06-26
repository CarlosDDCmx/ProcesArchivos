from menu.menu import Menu
from menu.commands.concrete_command import ExitCommand, SayHelloCommand
from menu.commands.submenu_command import SubMenuCommand
from menu.menus.tools_menu import build_tools_menu
from utils.i18n.safe import safe_gettext as _

def build_main_menu():
    menu = Menu(title=_("menu_prin"))
    menu.add_command("1", SubMenuCommand(_("herramientas"), build_tools_menu), _("herramientas"))
    menu.add_command("2", SayHelloCommand(), _("saludar"))
    return menu
