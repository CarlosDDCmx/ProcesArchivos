from menu.navigator import Navigator
from menu.menu import Menu

def dummy_menu(title):
    """Crea un menú falso con un título dado (para pruebas)."""
    return Menu(title=title)

# ──────────────────────────────────────────────────────────────────────────────
# Pruebas para get_breadcrumb()
# ──────────────────────────────────────────────────────────────────────────────

def test_get_breadcrumb_short_stack():
    """Muestra todo el breadcrumb si hay 3 o menos niveles."""
    nav = Navigator()
    nav.stack = [
        dummy_menu("Inicio"),
        dummy_menu("Submenú")
    ]
    assert nav.get_breadcrumb() == "Inicio→Submenú"

def test_get_breadcrumb_expanded():
    """Fuerza breadcrumb expandido aunque sea largo."""
    nav = Navigator()
    nav.stack = [
        dummy_menu("Inicio"),
        dummy_menu("Paso 1"),
        dummy_menu("Paso 2"),
        dummy_menu("Final")
    ]
    nav.expand_breadcrumb = True
    assert nav.get_breadcrumb() == "Inicio→Paso 1→Paso 2→Final"

def test_get_breadcrumb_compressed():
    """Comprueba breadcrumb comprimido automáticamente con muchos niveles."""
    nav = Navigator()
    nav.stack = [
        dummy_menu("Inicio"),
        dummy_menu("Medio 1"),
        dummy_menu("Medio 2"),
        dummy_menu("Final")
    ]
    nav.expand_breadcrumb = False
    assert nav.get_breadcrumb() == "Inicio→…→Final"

# ──────────────────────────────────────────────────────────────────────────────
# Pruebas para replace()
# ──────────────────────────────────────────────────────────────────────────────

def test_replace_current_with_callable():
    """Reemplaza el menú actual usando un constructor (función)."""
    nav = Navigator()
    nav.go_to(dummy_menu("Original"))
    nav.replace_current(lambda: dummy_menu("Reemplazo"))
    assert nav.stack[-1].title == "Reemplazo"

def test_replace_current_with_instance():
    """Reemplaza el menú actual usando una instancia directa."""
    nav = Navigator()
    nav.go_to(dummy_menu("Original"))
    nuevo = dummy_menu("Instancia")
    nav.replace_current(nuevo)
    assert nav.stack[-1].title == "Instancia"

def test_replace_current_with_empty_stack_logs_error(caplog):
    """No hace nada si la pila está vacía."""
    nav = Navigator()
    nav.stack.clear()
    nav.replace_current(dummy_menu("Ignorado"))
    assert "no se puede mostrar el menú" in caplog.text.lower()

# ──────────────────────────────────────────────────────────────────────────────
# Pruebas para back()
# ──────────────────────────────────────────────────────────────────────────────

def test_back_removes_last_menu_and_shows_previous(monkeypatch):
    """El método back() remueve el menú actual y muestra el anterior."""
    nav = Navigator()
    m1 = dummy_menu("Menú 1")
    m2 = dummy_menu("Menú 2")

    # Navegamos a ambos menús
    nav.go_to(m1)
    nav.go_to(m2)

    # Parcheamos show() para que no entre en loop
    monkeypatch.setattr(Menu, "show", lambda self, nav: None)

    # Llamamos back() y verificamos
    nav.back()
    assert len(nav.stack) == 1
    assert nav.stack[-1].title == "Menú 1"

def test_back_with_one_menu_does_nothing(monkeypatch):
    """No hace nada si solo hay un menú en la pila."""
    nav = Navigator()
    nav.go_to(dummy_menu("Único"))

    monkeypatch.setattr(Menu, "show", lambda self, nav: None)
    nav.back()
    assert len(nav.stack) == 1
    assert nav.stack[-1].title == "Único"