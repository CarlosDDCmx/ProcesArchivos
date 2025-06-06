import logging
import tempfile
from core.logger import LoggerManager

def test_logger_writes_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        log_path = tmp.name

    logger = LoggerManager.get_logger(log_file=log_path, log_level="DEBUG", enable_logging=True)
    logger.debug("Mensaje de prueba")

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Mensaje de prueba" in content
