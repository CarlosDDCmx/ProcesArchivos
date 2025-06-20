from menu.menu import Menu
from menu.commands.concrete_command import BackCommand
from menu.commands.detect_file_command import DetectFileCommand
from utils.i18n.safe import safe_gettext as _

def build_detector_menu():
    menu = Menu(title=_("detector"))
    menu.add_command("1", DetectFileCommand(), _("detec_info"))
    menu.add_command("0", BackCommand(), _("volver"))
    return menu