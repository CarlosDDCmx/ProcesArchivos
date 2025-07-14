import pytest
from menu.menu import Menu
from menu.commands.concrete_command import (
    ExitCommand,
    ShowResultsCommand,
    MemoryInspectCommand,
    SelectActiveCommand,
)
from menu.commands.base import Command

# 🔧 TEST 1: Verifica que se agregan todos los comandos universales si el menú está vacío
def test_inject_universal_adds_all_commands():
    menu = Menu("Universal Test")
    assert len(menu.commands) == 0  # Aún no se agregan

    menu._inject_universal()

    # Verifica que se agregaron los comandos esperados
    assert "x" in menu.commands
    assert "r" in menu.commands
    assert "m" in menu.commands
    assert "s" in menu.commands

    # Verifica que sean del tipo esperado
    assert isinstance(menu.commands["x"][0], ExitCommand)
    assert isinstance(menu.commands["r"][0], ShowResultsCommand)
    assert isinstance(menu.commands["m"][0], MemoryInspectCommand)
    assert isinstance(menu.commands["s"][0], SelectActiveCommand)

# 🔧 TEST 2: Verifica que no se sobrescriben comandos existentes
def test_inject_universal_does_not_override_existing():
    class CustomCommand(Command):
        def execute(self, navigator): pass

    menu = Menu("Menú Personalizado")
    custom_cmd = CustomCommand()

    # Se agrega un comando que colisiona con uno universal
    menu.add_command("x", custom_cmd, "Personalizado")

    menu._inject_universal()

    # Debe conservar el comando personalizado
    assert menu.commands["x"][0] is custom_cmd
