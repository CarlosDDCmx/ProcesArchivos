from typing import List, Dict, Any, Optional
from utils.i18n.safe import safe_gettext as _

def _normalize_ext(ext: str) -> str:
    """Devuelve la extensión en minúsculas SIN el punto inicial."""
    return ext.lower().lstrip(".")

def detect_with_heuristics(
    header: bytes,
    file_path: str,
    extension: str,
    mime_type: Optional[str],
    ambiguous_signatures: List[Dict[str, Any]],
) -> Optional[str]:
    """
    Devuelve el tipo detectado combinando:
      • cabecera (hex)
      • extensión (normalizada, sin punto, minúsc.)
      • MIME (minúsc.)
    """
    norm_ext = _normalize_ext(extension)
    norm_mime = (mime_type or "").lower()

    for entry in ambiguous_signatures:
        magic = bytes.fromhex(entry["magic"].lower())

        if not header.startswith(magic):
            continue  # cabecera no coincide → siguiente firma

        # Extensiones y MIME en la firma ya vienen normalizados (.json)
        ext_match = norm_ext and norm_ext in [e.lstrip(".").lower() for e in entry.get("extensions", [])]
        mime_match = norm_mime and norm_mime in [m.lower() for m in entry.get("mime_types", [])]

        # Basta UNA coincidencia para considerarlo resuelto
        if ext_match or mime_match:
            return _(entry["detected_type"])

    return None
