import gettext
import locale
import os
import builtins

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "locale")
DEFAULT_LANG = "es"
_translation = None

def get_translator(lang_code=None):
    """Carga el traductor para el idioma dado y lo asigna a builtins._"""
    global _translation
    lang = lang_code or _get_system_lang()
    try:
        _translation = gettext.translation(
            "messages", localedir=LOCALE_DIR, languages=[lang], fallback=False
        )
    except FileNotFoundError:
        print(f"⚠️  Archivo de traducción no encontrado para '{lang}', usando idioma original (msgid).")
        _translation = gettext.translation(
            "messages", localedir=LOCALE_DIR, languages=[lang], fallback=True
        )

    builtins._ = _translation.gettext
    return _translation.gettext

def _get_system_lang():
    """Obtiene el código de idioma del sistema."""
    try:
        return locale.getdefaultlocale()[0][:2]
    except Exception:
        return DEFAULT_LANG