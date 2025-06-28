from pathlib import Path
import logging
from typing import List

from utils.i18n.safe import safe_gettext as _
from .base import Command
from memory import get_active_event
from memory.events import DetectedFamily
from ofimatic import read_opendocument, read_docx

class ReadODFCommand(Command):
    """Lee y muestra el texto de un documento OpenDocument (ODT/ODS/ODP)."""

    def execute(self, navigator):
        active = get_active_event()
        if not active or active.family is not DetectedFamily.OPENDOCUMENT:
            logging.warning(_("sin_resultados"))
            return
        path = active.path
        if path is None:
            logging.warning(_("sin_resultados"))
            return

        try:
            paragraphs: List[str] = read_opendocument(path)
            logging.info(_("odf_leido").format(parrafos=len(paragraphs)))
            print("\n".join(paragraphs))
        except Exception as exc:
            logging.error(_("docx_error_lectura").format(error=str(exc)))


class ReadDOCXCommand(Command):
    """Lee y muestra el texto de un documento DOCX."""

    def execute(self, navigator):
        active = get_active_event()
        if not active or active.family is not DetectedFamily.OFFICE_ZIP:
            logging.warning(_("sin_resultados"))
            return
        path = active.path
        if path is None:
            logging.warning(_("sin_resultados"))
            return

        try:
            paragraphs: List[str] = read_docx(path)
            logging.info(_("docx_leido").format(parrafos=len(paragraphs)))
            print("\n".join(paragraphs))
        except Exception as exc:
            logging.error(_("docx_error_lectura").format(error=str(exc)))
