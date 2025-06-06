import logging
from typing import Optional

class LoggerManager:
    _logger_instance: Optional[logging.Logger] = None
    _log_path: Optional[str] = None

    @classmethod
    def get_logger(cls, log_file=None, log_level="INFO", enable_logging=True) -> logging.Logger:
        if cls._logger_instance is not None:
            return cls._logger_instance

        logger = logging.getLogger("document_processor")
        logger.setLevel(log_level.upper())
        logger.handlers.clear()

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        if enable_logging:
            log_file_path = log_file or "app.log"
            cls._log_path = log_file_path
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        cls._logger_instance = logger
        return logger

    @classmethod
    def get_log_path(cls) -> Optional[str]:
        return cls._log_path
