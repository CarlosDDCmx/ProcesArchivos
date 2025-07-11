"""
Punto de entrada centralizado para manejar distintos formatos ofimáticos.

Expone:
    - get_format_handler(mime_type: str) → Dict[str, Callable]
    - SUPPORTED_FORMATS → Dict con los tipos soportados
"""

from .formats.docx import read_docx, stats_docx, metadata_docx
from .loader_opendoc import read_opendocument, stats_opendoc, metadata_opendoc
from utils.i18n.safe import safe_gettext as _

# 📦 Mapeo MIME → funciones asociadas
SUPPORTED_FORMATS: dict[str, dict] = {
    # ─── OpenDocument Formats ─────────────────────────────
    "application/vnd.oasis.opendocument.text": {
        "type": "odt",
        "read": read_opendocument,
        "stats": stats_opendoc,
        "metadata": metadata_opendoc,
    },
    "application/vnd.oasis.opendocument.spreadsheet": {
        "type": "ods",
        "read": read_opendocument,
        "stats": stats_opendoc,
        "metadata": metadata_opendoc,
    },
    "application/vnd.oasis.opendocument.presentation": {
        "type": "odp",
        "read": read_opendocument,
        "stats": stats_opendoc,
        "metadata": metadata_opendoc,
    },

    # ─── Microsoft Office OpenXML (DOCX, XLSX, PPTX) ───────
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
        "type": "docx",
        "read": read_docx,
        "stats": stats_docx,
        "metadata": metadata_docx,
    },

    # En el futuro:
    # "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
    #     "type": "xlsx",
    #     "read": read_xlsx,
    #     "stats": stats_xlsx,
    #     "metadata": metadata_xlsx,
    # },

    # "application/vnd.openxmlformats-officedocument.presentationml.presentation": {
    #     "type": "pptx",
    #     "read": read_pptx,
    #     "stats": stats_pptx,
    #     "metadata": metadata_pptx,
    # },
}

# ── Acceso seguro por MIME ──────────────────────────────────
def get_format_handler(mime_type: str | None) -> dict:
    """
    Devuelve el handler de funciones correspondiente al MIME.
    Lanza KeyError si no está soportado.
    """
    if mime_type in SUPPORTED_FORMATS:
        return SUPPORTED_FORMATS[mime_type]
    raise KeyError(_("formato_no_soportado").format(mime_type=mime_type))
