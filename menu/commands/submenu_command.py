from .base import Command
from utils.i18n.safe import safe_gettext as _

class SubMenuCommand(Command):
    def __init__(self, name, submenu_builder):
        self.name = name
        self.submenu_builder = submenu_builder

    def execute(self, navigator):
        if self.submenu_builder:
            submenu = self.submenu_builder()
            navigator.go_to(submenu)
        else:
            print(_("volver"))