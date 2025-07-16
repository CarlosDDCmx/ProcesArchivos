import pytest
from ofimatic.loader_dispatch import get_format_handler, SUPPORTED_FORMATS
from utils.i18n.safe import safe_gettext as _

# Prueba que todos los tipos MIME definidos tienen las claves necesarias
def test_supported_formats_structure():
    required_keys = {"type", "read", "stats", "metadata"}
    for mime, entry in SUPPORTED_FORMATS.items():
        assert isinstance(entry, dict), f"{mime} debe ser un dict"
        assert required_keys.issubset(entry.keys()), f"{mime} debe tener las claves {required_keys}"

# Prueba que get_format_handler retorna el handler correcto para cada tipo conocido
@pytest.mark.parametrize("mime_type", list(SUPPORTED_FORMATS.keys()))
def test_get_format_handler_valid(mime_type):
    handler = get_format_handler(mime_type)
    assert isinstance(handler, dict)
    assert "read" in handler
    assert callable(handler["read"])

# Prueba que get_format_handler lanza KeyError para tipos no soportados
def test_get_format_handler_invalid():
    with pytest.raises(KeyError) as exc:
        get_format_handler("application/unknown")

    expected_msg = _("formato_no_soportado").split("{")[0].strip()
    assert expected_msg in str(exc.value)
