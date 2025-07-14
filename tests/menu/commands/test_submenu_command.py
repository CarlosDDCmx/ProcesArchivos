#  Pruebas para el comando SubMenuCommand que permite navegar hacia submenús.

import pytest
from menu.commands.submenu_command import SubMenuCommand
from menu.menu import Menu
from menu.navigator import Navigator
from unittest.mock import patch

# Verifica que SubMenuCommand navega correctamente al submenú deseado
@patch("menu.menu.Menu.show")  # Evita que show() entre al bucle interactivo
def test_submenu_command_navigates_to_submenu(mock_show):
    navigator = Navigator()
    submenu = Menu("Herramientas")
    command = SubMenuCommand("Herramientas", lambda: submenu)
    
    command.execute(navigator)

    assert len(navigator.stack) == 1
    assert navigator.stack[-1].title == "Herramientas"
    mock_show.assert_called_once()

# Verifica que SubMenuCommand muestra mensaje cuando no hay submenú asignado
@patch("menu.menu.Menu.show")  # Garantiza que no se muestre ningún menú real
def test_submenu_command_prints_if_no_builder(mock_show, capsys):
    navigator = Navigator()
    command = SubMenuCommand("Herramientas", None)
    
    command.execute(navigator)

    output = capsys.readouterr().out
    assert "volver" in output.lower()
    mock_show.assert_not_called()
