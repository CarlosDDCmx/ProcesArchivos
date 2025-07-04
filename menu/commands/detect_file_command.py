from .base import Command
from utils.i18n.safe import safe_gettext as _
from detector.analyzer import detect_file_type
from memory.bus import MemoryBus
from memory.events import FileAnalyzed
from detector.family import map_family
from pathlib import Path
import logging


class DetectFileCommand(Command):
    def execute(self, navigator):
        file_path = input(_("ruta_entra")).strip()
        if not file_path:
            logging.warning(_("detector_no_ruta"))
            return

        header_bytes_input = input(_("bytes_entra")).strip()
        header_bytes = 8 if not header_bytes_input else int(header_bytes_input or 8)

        try:
            results = detect_file_type(file_path, header_bytes=header_bytes, logger=logging)
            evt = FileAnalyzed(
                path=Path(file_path),
                detected_type=results["detected_type"],
                family=map_family(results["detected_type"]),
                metadata=results,
            )
            MemoryBus.emit(evt)
            logging.info(_("result_detector"))
            for key, value in results.items():
                print(f"{key}: {value}")

            # Marcar como activo y refrescar menú
            from memory import set_active_event
            from menu.menus.tools_menu import build_tools_menu

            set_active_event(evt)
            navigator.replace_current(build_tools_menu)

        except Exception as exc:
            logging.error(_("detector_falla").format(error=str(exc)))
