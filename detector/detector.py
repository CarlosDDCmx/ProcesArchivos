import json
import mimetypes
import os
from typing import Dict, Any

from utils.i18n.safe import safe_gettext as _


# Ruta a las firmas mágicas
SIGNATURES_PATH = os.path.join(os.path.dirname(__file__), "data", "signatures.json")

# Carga inicial de firmas en memoria
MAGIC_HEADERS: Dict[bytes, str] = {}
try:
    with open(SIGNATURES_PATH, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
        MAGIC_HEADERS = {bytes.fromhex(k): v for k, v in raw.items()}
except Exception as exc:
    print(_("error_firmas_carga").format(error=str(exc)))


def load_signatures() -> Dict[bytes, str]:
    """Devuelve el diccionario global de firmas ya cargadas."""
    return MAGIC_HEADERS


def detect_from_header(header: bytes, signatures: Dict[bytes, str]) -> str:
    """Identifica un tipo de archivo comparando la cabecera con las firmas."""
    for magic, filetype in signatures.items():
        if header.startswith(magic):
            return _(filetype)
    return _("desconocido")


def detect_file_type(file_path: str, logger=None) -> Dict[str, Any]:
    """
    Devuelve metadatos + tipo detectado usando solo firmas claras.
    """
    try:
        # ── Leer encabezado y tamaño ───────────────────────────────────
        with open(file_path, "rb") as fh:
            header = fh.read(8)
            fh.seek(0, os.SEEK_END)
            size = fh.tell()

        # ── Metadatos básicos ──────────────────────────────────────────
        mime_type, _ = mimetypes.guess_type(file_path)
        extension = os.path.splitext(file_path)[1].lower()
        detected_type = detect_from_header(header, load_signatures())

        return {
            "path": file_path,
            "size": size,
            "header": header.hex(),
            "extension": extension,
            "mime_type": mime_type,
            "detected_type": detected_type,
        }

    except Exception as exc:
        if logger:
            logger.error(_("detector_error_lee").format(error=exc))
        raise
