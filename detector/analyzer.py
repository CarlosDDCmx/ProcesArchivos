import mimetypes
import os
from typing import Dict, List, Any, Optional
from .loader import load_signatures          # carga JSON de firmas
from .report import report_result            # reporter para logging
from .heuristics import detect_with_heuristics
from utils.i18n.safe import safe_gettext as _

def detect_from_header(
    header: bytes,
    file_path: str,
    extension: str,
    mime_type: Optional[str],
    signatures: Dict[bytes, str],
    ambiguous_signatures: List[Dict[str, Any]],
) -> str:
    """
    Devuelve el tipo detectado a partir de la cabecera y metadatos.

    1. Comprueba primero firmas ambiguas (mismo prefijo pero contexto distinto).
    2. Luego busca coincidencia exacta en las firmas “claras”.
    3. Por último aplica heurísticas especiales.
    """
    # ── 1. Firmas ambiguas ───────────────────────────────────────────────
    for entry in ambiguous_signatures:
        magic_hex = entry.get("magic", "")
        if magic_hex and not header.startswith(bytes.fromhex(magic_hex)):
            continue
        if extension in entry.get("extensions", []) or mime_type in entry.get("mime_types", []):
            return _(entry["detected_type"])

    # ── 2. Firmas claras ────────────────────────────────────────────────
    for magic, filetype in signatures.items():
        if header.startswith(magic):
            return _(filetype)

    # ── 3. Heurística de último recurso ────────────────────────────────
    return detect_with_heuristics(
        header, file_path, extension, mime_type, ambiguous_signatures
    ) or _("desconocido")


def detect_file_type(
    file_path: str,
    header_bytes: int = 8,
    logger=None,
) -> Dict[str, Any]:
    """
    Analiza un archivo y devuelve un dict con metadatos + tipo detectado.

    Args:
        file_path: Ruta al archivo.
        header_bytes: Número de bytes a leer del encabezado.
        logger: Instancia de logger compatible con `logging.Logger`.
    """
    try:
        # ── Lectura de encabezado y tamaño ──────────────────────────────
        with open(file_path, "rb") as fh:
            header = fh.read(header_bytes)
            actual_bytes_read = len(header)
            fh.seek(0, os.SEEK_END)
            size = fh.tell()

        if actual_bytes_read < header_bytes:
            warning = _("reporte_bytes_insuf").format(
                requested=header_bytes, actual=actual_bytes_read
            )
            logger.warning(warning) if logger else print(warning)

        # ── Metadatos básicos ───────────────────────────────────────────
        mime_type, _ = mimetypes.guess_type(file_path)
        extension = os.path.splitext(file_path)[1].lower()

        # ── Firma + heurística ──────────────────────────────────────────
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

        # ── Reporte opcional al logger ──────────────────────────────────
        if logger:
            report_result(result, logger)

        return result

    except Exception as exc:
        if logger:
            logger.error(_("detector_error_lee").format(error=exc))
        raise
