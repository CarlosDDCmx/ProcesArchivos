from memory.events import (
    Event, FileAnalyzed, OfficeDocAnalyzed, ImageAnalyzed, ErrorEvent, DetectedFamily
)
from pathlib import Path

# ── Prueba: creación y atributos básicos de FileAnalyzed ────────────────
def test_file_analyzed_event():
    path = Path("archivo.txt")
    event = FileAnalyzed(
        path=path,
        detected_type="text/plain",
        family=DetectedFamily.UNKNOWN,
        metadata={"author": "Juan"}
    )
    assert event.path == path
    assert event.detected_type == "text/plain"
    assert event.family == DetectedFamily.UNKNOWN
    assert event.metadata["author"] == "Juan"
    assert isinstance(event, Event)

# ── Prueba: creación de evento OfficeDocAnalyzed con atributos extra ────
def test_office_doc_analyzed_event():
    event = OfficeDocAnalyzed(
        path=Path("doc.odt"),
        detected_type="application/vnd.oasis.opendocument.text",
        family=DetectedFamily.OPENDOCUMENT,
        metadata={},
        paragraphs=10,
        tables=2,
        embedded_objects=1
    )
    assert event.paragraphs == 10
    assert event.tables == 2
    assert event.embedded_objects == 1
    assert isinstance(event, FileAnalyzed)
    assert isinstance(event, Event)

# ── Prueba: creación de evento ImageAnalyzed con datos de imagen ───────
def test_image_analyzed_event():
    event = ImageAnalyzed(
        path=Path("imagen.jpg"),
        detected_type="image/jpeg",
        family=DetectedFamily.IMAGE,
        metadata={},
        width=1920,
        height=1080,
        color_space="RGB",
        exif={"ISO": 100}
    )
    assert event.width == 1920
    assert event.height == 1080
    assert event.color_space == "RGB"
    assert event.exif["ISO"] == 100
    assert isinstance(event, FileAnalyzed)
    assert isinstance(event, Event)

# ── Prueba: creación de evento de error ─────────────────────────────────
def test_error_event():
    event = ErrorEvent(origin="lector", message="Archivo no válido")
    assert event.origin == "lector"
    assert event.message == "Archivo no válido"
    assert isinstance(event, Event)
