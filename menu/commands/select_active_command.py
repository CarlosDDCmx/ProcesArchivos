import logging
from typing import List
from utils.i18n.safe import safe_gettext as _
from .base import Command
from memory import list_events, set_active_event
from menu.navigator import Navigator


class SelectActiveCommand(Command):
    """Lista los archivos analizados y permite seleccionar el activo."""

    def execute(self, navigator: Navigator):
        eventos: List = list_events()
        if not eventos:
            print(_("sin_resultados"))
            return

        # Muestra lista numerada
        print(_("seleccionar_archivo_titulo"))
        for idx, evt in enumerate(eventos, 1):
            print(f"{idx}. {evt.path}  →  {evt.detected_type}")

        try:
            choice = int(input(_("eleccion_entra")))
            if not 1 <= choice <= len(eventos):
                raise ValueError
        except ValueError:
            print(_("error_no_valido"))
            return

        set_active_event(eventos[choice - 1])
        logging.info(_("archivo_activo_cambiado").format(path=eventos[choice - 1].path))

        # Refresca el menú actual para que se actualicen las opciones
        from menu.menus.tools_menu import build_tools_menu
        navigator.replace_current(build_tools_menu)
