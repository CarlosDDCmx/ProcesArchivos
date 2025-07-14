import pytest
import shutil
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from menu.navigator import Navigator
from menu.menus.main_menu import build_main_menu
from menu.menus.tools_menu import build_tools_menu
from tests.helpers import ExitLoop

@pytest.fixture
def isolated_locale(tmp_path):
    """
    Crea una copia temporal aislada de los archivos .po y .pot en tmp_path.
    Cambia el directorio actual a tmp_path durante la prueba.
    """
    # Rutas originales
    locale_src = Path("locale")
    pot_src = Path("messages.pot")

    # Rutas destino temporales
    locale_dst = tmp_path / "locale"
    pot_dst = tmp_path / "messages.pot"

    # Copiar directorio locale
    if locale_src.exists():
        shutil.copytree(locale_src, locale_dst)
    else:
        locale_dst.mkdir(parents=True)

    # Copiar archivo .pot
    if pot_src.exists():
        shutil.copy2(pot_src, pot_dst)

    # Cambiar working directory
    old_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        yield tmp_path  # Aquí ocurre la prueba
    finally:
        os.chdir(old_cwd)

class ExitLoop(Exception):
    """Excepción personalizada para simular sys.exit en tests."""
    pass

@pytest.fixture(autouse=True)
def patch_sys_exit(monkeypatch):
    """Parchea sys.exit para que no cierre pytest, sino que lance ExitLoop."""
    def fake_exit(code=0):
        raise ExitLoop()
    monkeypatch.setattr("sys.exit", fake_exit)
    yield

@pytest.fixture
def nav_with_main_menu():
    """Crea Navigator con menú principal cargado, sin mostrarlo automáticamente."""
    navigator = Navigator()
    menu = build_main_menu()
    navigator.stack.append(menu)
    return navigator

@pytest.fixture
def mock_user_input(monkeypatch):
    def _mock_input_sequence(inputs):
        gen = (i for i in inputs)
        monkeypatch.setattr("builtins.input", lambda _: next(gen))
    return _mock_input_sequence

def test_user_navigates_and_says_hello(nav_with_main_menu, mock_user_input, capsys):
    mock_user_input(["2", "x"])  # SayHello + salir

    from menu.commands.concrete_command import ExitCommand
    with patch.object(ExitCommand, "execute", return_value=None):
        menu = nav_with_main_menu.stack[-1]
        menu.show(nav_with_main_menu)

    out = capsys.readouterr().out
    assert "hola" in out.lower()

@pytest.fixture
def nav_with_tools_menu_mocked():
    """Fixture que retorna un Navigator con tools_menu construido con un archivo activo simulado."""
    mock_event = MagicMock()
    mock_event.metadata = {
        "mime_type": "application/vnd.oasis.opendocument.text"
    }

    mock_format_handler = {
        "type": "odt",
        "stats": True,
        "metadata": True
    }

    with patch("menu.menus.tools_menu.get_active_event", return_value=mock_event), \
         patch.dict("menu.menus.tools_menu.SUPPORTED_FORMATS", {
             "application/vnd.oasis.opendocument.text": mock_format_handler
         }):
        
        nav = Navigator()
        tools_menu = build_tools_menu()
        nav.go_to(tools_menu)
        yield nav