import os
import logging
from utils.logger.core import configure_logger

def test_configure_logger_console_only(capsys):
    logger = configure_logger(verbose=True, log_to_file=False, name="testLogger_console")
    logger.info("Mensaje de prueba")
    captured = capsys.readouterr()
    assert "Mensaje de prueba" in captured.err  # Se captura stderr en lugar de stdout

def test_configure_logger_to_file(tmp_path):
    log_dir = tmp_path / "logs"
    logger = configure_logger(
        verbose=False,
        log_to_file=True,
        log_path=log_dir,
        name="fileLogger"
    )
    logger.warning("Warning desde prueba")

    # Buscar archivo de log creado
    files = list(log_dir.glob("*.log"))
    assert files, "No se creó el archivo de log"
    contenido = files[0].read_text(encoding="utf-8")
    assert "Warning desde prueba" in contenido

def test_logger_fallback_if_dir_invalid(monkeypatch):
    def fail_makedirs(*args, **kwargs):
        raise OSError("No se puede crear directorio")

    monkeypatch.setattr("os.makedirs", fail_makedirs)

    # Esto imprimirá un error pero no lanzará excepción
    logger = configure_logger(log_to_file=True, log_path="/no_existe/ruta")
    assert isinstance(logger, logging.Logger)
