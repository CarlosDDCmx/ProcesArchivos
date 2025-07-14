import gettext
import locale
import os
import builtins
import sys

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "locale")
DEFAULT_LANG = "es"

def get_translator(lang: str | None = None):
    """Inicializa gettext y devuelve una función de traducción (_)."""
    if lang is None:
        lang_tuple = locale.getlocale()
        lang = lang_tuple[0] if lang_tuple and lang_tuple[0] else DEFAULT_LANG

    lang = lang.split("_")[0].lower()  # Normalizar a 'es', 'en', etc.

    safe_print(
        f"🌐 Idioma del sistema detectado: {lang}",
        f"[i18n] Idioma del sistema detectado: {lang}"
    )

    try:
        translator = gettext.translation(
            domain="messages",
            localedir=LOCALE_DIR,
            languages=[lang],
            fallback=True
        )
        return translator.gettext
    except Exception as e:
        safe_print(
            f"⚠️  Error al cargar traducciones: {e}",
            f"[i18n] Error al cargar traducciones: {e}"
        )
        return lambda s: s  # Fallback sin traducción


def _get_system_lang():
    """
    Obtiene el código de idioma del sistema, compatible con futuras versiones de Python.
    Usa locale.getlocale() y getlocale(locale.LC_MESSAGES) si es posible.
    """
    try:
        # Primero intenta con LC_MESSAGES, si está disponible (Unix y algunos sistemas Windows)
        lang_info = locale.getlocale(locale.LC_MESSAGES)
        if not lang_info or not lang_info[0]:
            lang_info = locale.getlocale()  # Fallback general

        lang_code = lang_info[0][:2].lower() if lang_info and lang_info[0] else DEFAULT_LANG
        return lang_code
    except Exception:
        return DEFAULT_LANG
    
def supports_unicode() -> bool:
    """Detecta si la salida estándar permite Unicode extendido (como emojis)."""
    encoding = sys.stdout.encoding or ""
    return encoding.lower().startswith("utf")  # Ej: utf-8

def safe_print(msg_with_emoji: str, msg_plain: str):
    """
    Imprime una versión con o sin emoji según soporte del sistema.
    - msg_with_emoji: mensaje decorado con emojis.
    - msg_plain: mensaje simple alternativo.
    """
    print(msg_with_emoji if supports_unicode() else msg_plain)