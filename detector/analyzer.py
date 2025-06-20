import mimetypes
import os
from .loader import load_signatures
from .report import report_result
from utils.i18n.safe import safe_gettext as _

def detect_from_header(header: bytes, file_path: str, signatures: dict):
    for magic, filetype in signatures.items():
        if header.startswith(magic):
            return _(filetype)
    return _("desconocido")

def detect_file_type(file_path: str, header_bytes: int = 8, logger=None): 
    try:
        with open(file_path, "rb") as f:
            header = f.read(header_bytes)
            actual_bytes_read = len(header)

            f.seek(0, os.SEEK_END)
            size = f.tell()

        if actual_bytes_read < header_bytes:
            warning_msg = _("aviso_menor_bytes").format(
                requested=header_bytes, actual=actual_bytes_read
            )
            if logger:
                logger.warning(warning_msg)
            else:
                print(warning_msg)

        mime_type, _ = mimetypes.guess_type(file_path)
        extension = os.path.splitext(file_path)[1].lower()
        signatures = load_signatures()
        detected_type = detect_from_header(header, file_path, signatures) or _("desconocido")

        result = {
            "path": file_path,
            "size": size,
            "header": header.hex(),
            "header_bytes": header_bytes,
            "extension": extension,
            "mime_type": mime_type,
            "detected_type": detected_type,
        }

        if logger:
            report_result(result, logger)

        return result

    except Exception as e:
        if logger:
            logger.error(_("detector_error_lee").format(error=e))
        raise
