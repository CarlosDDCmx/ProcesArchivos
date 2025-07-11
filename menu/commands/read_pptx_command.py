import logging
from pathlib import Path
from typing import List

from utils.i18n.safe import safe_gettext as _
from .base import Command
from memory import get_active_event
from memory.events import DetectedFamily

# Placeholder
class ReadPPTXCommand(Command):
    """(Futuro) Lee y muestra contenido de un archivo PPTX."""

    def execute(self, navigator):
        active = get_active_event()
        if not active or active.family is not DetectedFamily.OFFICE_ZIP:
            logging.warning(_("sin_resultados"))
            return
        path = active.path
        if not path:
            logging.warning(_("sin_resultados"))
            return

        # TODO: Implementar lectura real de PPTX
        print(_("pptx_lectura_no_disponible"))
