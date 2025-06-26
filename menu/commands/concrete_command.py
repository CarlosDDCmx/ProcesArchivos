from .base import Command
from utils.i18n.safe import safe_gettext as _
from memory.subscribers import get_registry
from dataclasses import asdict
import sys, json
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

class ShowResultsCommand(Command):
    def execute(self, navigator):
        store = get_registry()
        if not store:
            print(_("sin_resultados"))
            return

        for fam, eventos in store.items():
            print(f"\n[{fam.name}]")
            for idx, evt in enumerate(eventos, 1):
                meta = evt.metadata
                print(f" {idx}. {meta['path']}  ->  {evt.detected_type}")

class MemoryInspectCommand(Command):
    def execute(self, navigator):
        registry = {
            fam.name: [asdict(evt) | {"path": str(evt.path), "family": evt.family.name}
                       for evt in eventos]
            for fam, eventos in get_registry().items()
        }
        print(json.dumps(registry, indent=2, ensure_ascii=False))