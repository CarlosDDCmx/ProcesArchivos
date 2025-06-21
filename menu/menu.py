import logging
from utils.i18n.safe import safe_gettext as _
from utils.static.menu import MENU_BANNER

class Menu:
    def __init__(self, title="Menu"):
        self.title = title
        self.commands = {}

    def add_command(self, key, command, description):
        self.commands[key] = (command, description)

    def display(self):
        print(f"\n{self.title}")
        print("-" * len(self.title))
        for key, (cmd, desc) in sorted(self.commands.items()):
            print(f"{key}. {desc}")

    def get_choice(self):
        try:
            return input(_("eleccion_entra")).strip()
        except EOFError:
            logging.warning(_("logger_cierre_inesp"))
        except Exception as e:
            logging.error(_("logger_error_entra").format(error=str(e)))
        return None

    def show(self, navigator):
        while True:
            print(MENU_BANNER)
            self.display()
            choice = self.get_choice()

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
                break
            else:
                print(_("error_no_valido"))
