# 🔹 Pruebas unitarias para el objeto Menu y sus métodos fundamentales.

import pytest
from menu.menu import Menu
from menu.commands.concrete_command import (
    ExitCommand, ShowResultsCommand, MemoryInspectCommand, SelectActiveCommand
)
from menu.commands.base import Command
from unittest.mock import patch
from io import StringIO


# Comando de prueba usado en múltiples tests
class DummyCommand(Command):
    def execute(self, navigator):
        navigator.executed = True


# Verifica que un comando se agregue correctamente al menú
def test_add_command():
    menu = Menu("Test")
    cmd = DummyCommand()
    menu.add_command("a", cmd, "Descripción")
    assert "a" in menu.commands
    assert menu.commands["a"][0] is cmd
    assert menu.commands["a"][1] == "Descripción"


# Verifica que el método display() imprima las opciones del menú
def test_display_prints_correctly(capsys):
    menu = Menu("Main Menu")
    menu.add_command("1", DummyCommand(), "Primera Opción")
    menu.display()
    captured = capsys.readouterr()
    assert "Main Menu" in captured.out
    assert "1. Primera Opción" in captured.out


# Simula entrada válida del usuario y evalúa el retorno
@patch("builtins.input", return_value="x")
def test_get_choice_success(mock_input):
    menu = Menu()
    choice = menu.get_choice()
    assert choice == "x"


# Simula un EOFError al pedir entrada, espera None y log registrado
@patch("builtins.input", side_effect=EOFError)
@patch("logging.warning")
def test_get_choice_eof(mock_log, mock_input):
    menu = Menu()
    choice = menu.get_choice()
    assert choice is None
    mock_log.assert_called_once()


# Simula una excepción general al pedir entrada, espera None y log registrado
@patch("builtins.input", side_effect=Exception("fallo"))
@patch("logging.error")
def test_get_choice_exception(mock_log, mock_input):
    menu = Menu()
    choice = menu.get_choice()
    assert choice is None
    mock_log.assert_called_once()


# Verifica que los comandos universales se agregan correctamente
def test_inject_universal_adds_all_commands():
    menu = Menu("Universal Test")
    assert len(menu.commands) == 0
    menu._inject_universal()

    expected = {
        "x": ExitCommand,
        "r": ShowResultsCommand,
        "m": MemoryInspectCommand,
        "s": SelectActiveCommand,
    }

    for key, expected_cls in expected.items():
        assert key in menu.commands
        command, description = menu.commands[key]
        assert isinstance(command, expected_cls)
        assert isinstance(description, str)
        assert description  # no está vacío


# Verifica que _inject_universal() no sobrescriba comandos existentes
def test_inject_universal_does_not_override_existing():
    class CustomCommand(Command):
        def execute(self, navigator): pass

    menu = Menu()
    custom_cmd = CustomCommand()
    menu.add_command("x", custom_cmd, "Personalizado")
    menu._inject_universal()

    assert menu.commands["x"][0] is custom_cmd
    assert menu.commands["x"][1] == "Personalizado"