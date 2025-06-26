from .base import Command
from utils.i18n.safe import safe_gettext as _
from detector.analyzer import detect_file_type
from memory import MemoryBus
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
        if not header_bytes_input:
            header_bytes = 8
        else:
            try:
                header_bytes = int(header_bytes_input)
                if header_bytes <= 0:
                    raise ValueError
            except ValueError:
                logging.error(_("error_bytes_tipo"))
                return

        try:
            results = detect_file_type(file_path, header_bytes=header_bytes, logger=logging)
            evt = FileAnalyzed(
                path=Path(file_path),
                detected_type=results["detected_type"],
                family=map_family(results["detected_type"]),
                metadata=results
            )
            MemoryBus.emit(evt)
            logging.info(_("result_detector"))
            for key, value in results.items():
                print(f"{key}: {value}")
        except Exception as e:
            logging.error(_("detector_falla").format(error=str(e)))