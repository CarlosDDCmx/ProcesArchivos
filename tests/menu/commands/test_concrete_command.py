#  Pruebas para el comando BackCommand que permite volver al menú anterior.

import pytest
from menu.commands.concrete_command import BackCommand
from menu.menu import Menu
from menu.navigator import Navigator
from unittest.mock import patch

# Verifica que BackCommand elimina el menú actual y muestra el anterior
@patch("menu.menu.Menu.show")  # Parchea Menu.show() para evitar input()
def test_back_command_goes_back(mock_show):
    nav = Navigator()
    m1 = Menu("Primero")
    m2 = Menu("Segundo")
    nav.stack.append(m1)
    nav.stack.append(m2)

    back = BackCommand()
    back.execute(nav)

    # Asegura que se eliminó el último menú (Segundo) y se mostró el anterior
    assert len(nav.stack) == 1
    assert nav.stack[-1].title == "Primero"
    mock_show.assert_called_once()
