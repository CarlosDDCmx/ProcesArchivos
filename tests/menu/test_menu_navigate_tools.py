import pytest
from unittest.mock import patch
from menu.commands.read_content_command import ReadContentCommand
from tests.helpers import ExitLoop

def test_navigate_to_tools_and_read_content(nav_with_main_menu, mock_user_input, capsys):
    # Simular entrada del usuario:
    # "1" → Herramientas
    # "2" → Leer contenido
    # "0" → Volver
    # "x" → Salir
    mock_user_input(["1", "2", "0", "x"])

    # Preparar mocks para que get_active_event devuelva un documento válido
    with patch("menu.menus.tools_menu.get_active_event") as mock_event, \
         patch.dict("menu.menus.tools_menu.SUPPORTED_FORMATS", {
             "application/vnd.oasis.opendocument.text": {
                 "type": "odt",
                 "stats": True,
                 "metadata": True,
             }
         }), \
         patch.object(ReadContentCommand, "execute", lambda self, nav: print(">> CONTENIDO LEÍDO")):

        # El mock del evento retorna un archivo activo con mime_type odt
        mock_event.return_value.metadata = {
            "mime_type": "application/vnd.oasis.opendocument.text"
        }

        try:
            nav_with_main_menu.stack[-1].show(nav_with_main_menu)
        except ExitLoop:
            pass  # Evita que sys.exit(0) detenga pytest

    output = capsys.readouterr().out.lower()
    assert "herramientas" in output
    assert "contenido leído" in output
    assert "volver" in output
