from detector.report import report_result
from unittest.mock import MagicMock

def test_report_result_logs_correctly():
    result = {
        "path": "/file.txt",
        "size": 1234,
        "header_bytes": 8,
        "header": "25504446",
        "extension": ".txt",
        "mime_type": "text/plain",
        "detected_type": "Texto plano",
    }

    mock_logger = MagicMock()
    report_result(result, mock_logger)

    assert mock_logger.info.call_count == 7
    mock_logger.info.assert_any_call(mock_logger.info.call_args_list[0][0][0])  # Confirma que se llamó con una cadena traducida
