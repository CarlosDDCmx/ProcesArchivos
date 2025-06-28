import mimetypes
import os
from .loader import load_signatures
from .report import report_result
from .heuristics import detect_with_heuristics
from utils.i18n.safe import safe_gettext as _

def detect_from_header(
    header: bytes,
    file_path: str,
    extension: str,
    mime_type: str,
    signatures: dict,
    ambiguous_signatures: list,
):
    for entry in ambiguous_signatures:
        magic_hex = entry.get("magic", "")
        if magic_hex and not header.startswith(bytes.fromhex(magic_hex)):
            continue

        if extension in entry.get("extensions", []) or mime_type in entry.get("mime_types", []):
            return _(entry["detected_type"])

    for magic, filetype in signatures.items():
        if header.startswith(magic):
            return _(filetype)

    return (
        detect_with_heuristics(header, file_path, extension, mime_type, ambiguous_signatures)
        or _("desconocido")
    )


def detect_file_type(file_path: str, header_bytes: int = 8, logger=None):
    try:
        with open(file_path, "rb") as f:
            header = f.read(header_bytes)
            actual_bytes_read = len(header)
            f.seek(0, os.SEEK_END)
            size = f.tell()

        if actual_bytes_read < header_bytes:
            warning_msg = _("reporte_bytes_insuf").format(
                requested=header_bytes, actual=actual_bytes_read
            )
            logger.warning(warning_msg) if logger else print(warning_msg)

        mime_type, _ = mimetypes.guess_type(file_path)
        extension = os.path.splitext(file_path)[1].lower()
        signatures, ambiguous = load_signatures()

        detected_type = detect_from_header(
            header, file_path, extension, mime_type, signatures, ambiguous
        )

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