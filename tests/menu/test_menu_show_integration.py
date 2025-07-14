import pytest
from menu.menu import Menu
from menu.navigator import Navigator
from menu.commands.base import Command
from unittest.mock import patch

# Excepción personalizada para evitar que sys.exit detenga las pruebas
class ExitLoop(Exception):
    pass

# Comando de prueba que registra si fue ejecutado
class TrackableCommand(Command):
    def __init__(self):
        self.executed = False

    def execute(self, navigator):
        self.executed = True

# Falso sys.exit que lanza una excepción controlada
def fake_exit(code=0):
    raise ExitLoop()

# Parametrizamos distintas combinaciones de entradas del usuario
@pytest.mark.parametrize("inputs", [
    ["", "z", "a", "x"],   # vacía, inválida, válida, salir
    ["a", "x"],            # válida y salir directamente
])
@patch("sys.exit", side_effect=fake_exit)
@patch("builtins.input")
def test_menu_show_executes_valid_command(mock_input, mock_exit, inputs):
    # Simula entradas del usuario
    mock_input.side_effect = inputs

    # Comando de prueba
    cmd = TrackableCommand()

    # Menú con un comando personalizado
    menu = Menu("Menú de Prueba")
    menu.add_command("a", cmd, "Comando de prueba")

    # Navegador simulado
    nav = Navigator()

    # Parchea _inject_universal para no interferir con la prueba
    with patch.object(menu, "_inject_universal"):
        try:
            menu.show(nav)
        except ExitLoop:
            pass

    # Verifica que el comando fue ejecutado
    assert cmd.executed is True

@patch("builtins.input", side_effect=["x"])
@patch("sys.exit", side_effect=fake_exit)
def test_menu_show_handles_exit_command(mock_exit, mock_input):
    # Crea menú con comandos universales activados
    menu = Menu("Menú de Salida")
    nav = Navigator()

    # Verifica que el comando "x" (salir) detona el flujo correcto
    with patch.object(menu, "_inject_universal"):
        menu.add_command("x", Command(), "Salir")
        with pytest.raises(ExitLoop):
            menu.show(nav)
