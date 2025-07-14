import pytest
from menu.navigator import Navigator
from menu.menu import Menu
from unittest.mock import MagicMock

# 🔍 TEST 1: Verifica que _show_current llama a show() del menú actual
def test_show_current_calls_menu_show(monkeypatch):
    # Crear un menú simulado con método show() espiado
    mock_menu = Menu("Menú de prueba")
    mock_show = MagicMock()
    monkeypatch.setattr(mock_menu, "show", mock_show)

    # Inicializar navigator y establecer el menú
    nav = Navigator()
    nav.stack.append(mock_menu)

    # Ejecutar método privado
    nav._show_current()

    # Verificar que show() fue llamado una vez con el navigator como argumento
    mock_show.assert_called_once_with(nav)

# 🔍 TEST 2: Si no hay menús en el stack, _show_current no lanza errores
def test_show_current_with_empty_stack_does_nothing():
    nav = Navigator()

    # Simplemente no debe lanzar excepción si el stack está vacío
    try:
        nav._show_current()
    except Exception as e:
        pytest.fail(f"_show_current lanzó una excepción con stack vacío: {e}")
