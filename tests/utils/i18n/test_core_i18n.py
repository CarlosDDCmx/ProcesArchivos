import builtins
from utils.i18n.core import get_translator

def test_get_translator_sets_builtin(monkeypatch):
    monkeypatch.delenv("LANG", raising=False)
    translator = get_translator("es")  # usa fallback si no encuentra
    assert callable(translator)
    assert builtins._("inicio_app") == translator("inicio_app")
    assert translator("inicio_app")  # puede devolver igual el msgid si no hay .mo
