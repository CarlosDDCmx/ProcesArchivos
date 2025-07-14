import builtins
from utils.i18n.safe import safe_gettext

def test_safe_gettext_fallback_if_no_builtin_underscore(monkeypatch):
    monkeypatch.delattr(builtins, "_", raising=False)
    assert safe_gettext("mensaje") == "mensaje"

def test_safe_gettext_uses_builtin_translation(monkeypatch):
    monkeypatch.setattr(builtins, "_", lambda msg: f"trad:{msg}")
    assert safe_gettext("hola") == "trad:hola"
