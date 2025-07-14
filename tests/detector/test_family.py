from detector.family import map_family
from memory.events import DetectedFamily

def test_family_office_zip():
    assert map_family("DOCX File") == DetectedFamily.OFFICE_ZIP

def test_family_opendocument():
    assert map_family("ODT File") == DetectedFamily.OPENDOCUMENT

def test_family_archive():
    assert map_family("7-ZIP File") == DetectedFamily.ARCHIVE

def test_family_pdf():
    assert map_family("PDF") == DetectedFamily.PDF

def test_family_image():
    assert map_family("PNG Image") == DetectedFamily.IMAGE

def test_family_audio():
    assert map_family("WAV Audio") == DetectedFamily.AUDIO

def test_family_video():
    assert map_family("MP4 Video") == DetectedFamily.VIDEO

def test_family_executable():
    assert map_family("ELF Executable") == DetectedFamily.EXECUTABLE

def test_family_unknown():
    assert map_family("Some Unknown Type") == DetectedFamily.UNKNOWN
