from menu.menu import Menu
from menu.commands.submenu_command import SubMenuCommand
from menu.commands.concrete_command import BackCommand
from menu.commands.detect_file_command import DetectFileCommand
#from menu.commands.opendoc_inspect_command import OpenDocInspectCommand
from memory.subscribers import family_exists
from memory.events import DetectedFamily
from utils.i18n.safe import safe_gettext as _

def build_tools_menu():
    menu = Menu(title=_("herramientas"))
    menu.add_command("1", DetectFileCommand(), _("detector"))

    if family_exists(DetectedFamily.OPENDOCUMENT):
        # menu.add_command("2", OpenDocInspectCommand(), _("leer_opendoc")) Para futuros modulos
        pass
    if family_exists(DetectedFamily.OFFICE_ZIP):
        # menu.add_command("3", OfficeZipCommand(), _("leer_office_zip")) Para futuros modulos
        pass

    menu.add_command("0", BackCommand(), _("volver"))
    return menu