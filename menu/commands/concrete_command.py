from .base import Command
import sys
from utils.i18n.safe import safe_gettext as _

class ExitCommand(Command):
    def execute(self, navigator):
        print(_("salir"))
        sys.exit(0)

class SayHelloCommand(Command):
    def execute(self, navigator):
        print(_("saluda_usuario"))

class BackCommand(Command):
    def execute(self, navigator):
        navigator.back()