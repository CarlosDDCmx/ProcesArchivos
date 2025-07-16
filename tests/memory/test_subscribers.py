import logging
from pathlib import Path
from unittest.mock import patch, MagicMock
from memory import subscribers
from memory.bus import MemoryBus
from memory.events import FileAnalyzed, OfficeDocAnalyzed, ErrorEvent, DetectedFamily


# ── Prueba: callback que guarda el evento usando add_event ──────────────
@patch("memory.subscribers.add_event")
def test_store_event(mock_add):
    evt = FileAnalyzed(
        path=Path("ejemplo.txt"),
        detected_type="text/plain",
        family=DetectedFamily.UNKNOWN,
        metadata={}
    )
    MemoryBus.emit(evt)
    mock_add.assert_called_once_with(evt)


# ── Prueba: callback que persiste evento en archivo JSON ────────────────
@patch("memory.subscribers.Path.write_text")
def test_persist_to_json(mock_write):
    evt = FileAnalyzed(
        path=Path("doc.txt"),
        detected_type="text/plain",
        family=DetectedFamily.ARCHIVE,
        metadata={"clave": "valor"}
    )
    MemoryBus.emit(evt)
    mock_write.assert_called_once()
    args, kwargs = mock_write.call_args
    assert '"clave": "valor"' in args[0]  # JSON generado


# ── Prueba: callback que registra errores en el log ─────────────────────
def test_log_error(caplog):
    evt = ErrorEvent(origin="validador", message="archivo dañado")
    with caplog.at_level(logging.ERROR):
        MemoryBus.emit(evt)
    assert "archivo dañado" in caplog.text
    assert "[validador]" in caplog.text
