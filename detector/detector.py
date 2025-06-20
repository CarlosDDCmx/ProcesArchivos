import mimetypes
import os
import json
from utils.i18n.safe import safe_gettext as _

SIGNATURES_PATH = os.path.join(os.path.dirname(__file__), "data", "signatures.json")

MAGIC_HEADERS = {}
try:
    with open(SIGNATURES_PATH, "r", encoding="utf-8") as f:
        signatures_raw = json.load(f)
        MAGIC_HEADERS = {bytes.fromhex(k): v for k, v in signatures_raw.items()}
except Exception as e:
    print(_("error_firmas_carga").format(error=str(e)))

def load_signatures():
    """Carga las firmas mágicas desde el archivo JSON."""
    return MAGIC_HEADERS

def detect_from_header(header: bytes, file_path: str, signatures: dict):
    """Compara una cabecera contra firmas mágicas para detectar el tipo de archivo."""
    for magic, filetype in signatures.items():
        if header.startswith(magic):
            return _(filetype)
    return _("desconocido")

def detect_file_type(file_path, logger=None):
    try:
        with open(file_path, "rb") as f:
            header = f.read(8)
            f.seek(0, os.SEEK_END)
            size = f.tell()

        mime_type, mime_type_2 = mimetypes.guess_type(file_path)
        extension = os.path.splitext(file_path)[1].lower()
        detected_type = detect_from_header(header, file_path, load_signatures())

        return {
            "path": file_path,
            "size": size,
            "header": header.hex(),
            "extension": extension,
            "mime_type": mime_type,
            "detected_type": detected_type,
        }

    except Exception as e:
        if logger:
            logger.error(_("detector_error_lee").format(error=e))
        raise
