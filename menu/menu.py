import logging
from .commands.base import Command
from utils.i18n.safe import safe_gettext as _
from utils.static.menu import MENU_BANNER

class Menu:
    def __init__(self, title="Menu"):
        self.title = title
        self.commands: dict[str, tuple[Command, str]] = {}

    def add_command(self, key, command, description):
        """Agrega un comando al menú actual."""
        self.commands[key.lower()] = (command, description)

    def _inject_universal(self):
        """Agrega comandos universales comunes a todos los menús."""
        from menu.commands.concrete_command import (
            ExitCommand, ShowResultsCommand, MemoryInspectCommand
        )
        from menu.commands.select_active_command import SelectActiveCommand
        universals = {
            "x": (ExitCommand(), _("salir_linea")),
            "r": (ShowResultsCommand(), _("ver_resultados")),
            "m": (MemoryInspectCommand(), _("ver_memoria")),
            "s": (SelectActiveCommand(), _("seleccionar_archivo")),
        }
        for k, v in universals.items():
            self.commands.setdefault(k, v)

    def display(self):
        """Muestra el menú por consola."""
        print(f"\n{self.title}")
        print("-" * len(self.title))
        for key, (cmd, desc) in sorted(self.commands.items()):
            print(f"{key}. {desc}")

    def get_choice(self):
        """Solicita al usuario su elección."""
        try:
            return input(_("eleccion_entra")).strip()
        except EOFError:
            logging.warning(_("logger_cierre_inesp"))
        except Exception as e:
            logging.error(_("logger_error_entra").format(error=str(e)))
        return None

    def show(self, navigator):
        """Loop de visualización e interacción del menú."""
        while True:
            print(MENU_BANNER)
            self._inject_universal() 
            self.display()
            choice = (self.get_choice() or "").lower() 

            if not choice:
                print(_("error_vacio"))
                continue

            if choice in self.commands:
                command, cmd = self.commands[choice]
                logging.debug(_("logger_menu_ele").format(choice=choice, menu=self.title))
                try:
                    command.execute(navigator)
                except Exception as e:
                    logging.exception(_("logger_error_eje_com").format(error=str(e)))
            else:
                print(_("error_no_valido"))
