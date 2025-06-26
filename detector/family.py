from memory.events import DetectedFamily

def map_family(det_type: str) -> DetectedFamily:
    t = det_type.upper()

    if "ZIP / DOCX" in t or "OPENXML" in t:
        return DetectedFamily.OFFICE_ZIP
    if "ZIP / ODT" in t or "OPENDOCUMENT" in t:
        return DetectedFamily.OPENDOCUMENT
    if "PDF" in t:
        return DetectedFamily.PDF
    if any(x in t for x in ("JPEG", "PNG", "GIF", "TIFF", "BMP")):
        return DetectedFamily.IMAGE
    if any(x in t for x in ("MP3", "FLAC", "AAC", "OGG", "WAV")):
        return DetectedFamily.AUDIO
    if any(x in t for x in ("AVI", "MP4", "MKV", "MPEG")):
        return DetectedFamily.VIDEO
    if any(x in t for x in ("ZIP", "RAR", "7-ZIP", "GZIP")):
        return DetectedFamily.ARCHIVE
    if any(x in t for x in ("EXE", "ELF", "WASM")):
        return DetectedFamily.EXECUTABLE
    return DetectedFamily.UNKNOWN
