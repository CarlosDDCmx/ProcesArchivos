from utils.i18n.safe import safe_gettext as _

def detect_with_heuristics(header: bytes, file_path: str, extension: str, mime_type: str, ambiguous_signatures: list):
    for entry in ambiguous_signatures:
        if header.startswith(bytes.fromhex(entry["magic"])):
            if extension in entry.get("extensions", []) or mime_type in entry.get("mime_types", []):
                return _(entry["detected_type"])
    return None
