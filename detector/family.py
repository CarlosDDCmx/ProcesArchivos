from memory.events import DetectedFamily

def map_family(det_type: str) -> DetectedFamily:
    t = det_type.upper()

    if "OFFICE‑OPENXML" in t:
        return DetectedFamily.OFFICE_ZIP
    if "OPENDOCUMENT" in t:
        return DetectedFamily.OPENDOCUMENT
    if "RAR" in t or "7‑ZIP" in t or "ZIP CIFRADO" in t:
        return DetectedFamily.ARCHIVE
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
    if any(x in t for x in ("ISO", "MDF", "MDS", "NRG", "DMG")):
        return DetectedFamily.DISK_IMAGES
    if any(x in t for x in ("EXE", "ELF", "WASM")):
        return DetectedFamily.EXECUTABLE
    return DetectedFamily.UNKNOWN
