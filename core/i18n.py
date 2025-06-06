import locale
import json
from pathlib import Path

_language_data = {}
_current_lang = "es"
DEFAULT_LANGUAGE = "es"

def get_default_language() -> str:
    """Detecta el idioma predeterminado del sistema (por ejemplo: 'es', 'en')."""
    lang, _ = locale.getdefaultlocale()
    return lang.split("_")[0] if lang else DEFAULT_LANGUAGE

def load_language(lang_code: str = None):
    """Carga el archivo de idioma existente, o crea uno vacío si no existe."""
    global _language_data, _current_lang

    _current_lang = lang_code or get_default_language()
    lang_path = Path(f"i18n/{_current_lang}.json")

    if not lang_path.exists():
        print(f"[i18n] Idioma '{_current_lang}' no tiene archivo de traducción.")
        print(f"[i18n] Generando archivo vacío en '{lang_path}'. Puedes traducirlo más adelante.")
        lang_path.parent.mkdir(parents=True, exist_ok=True)
        lang_path.write_text("{}", encoding="utf-8")

    try:
        with open(lang_path, encoding="utf-8") as f:
            _language_data = json.load(f)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar el archivo de idioma '{_current_lang}': {e}")
        print(f"[i18n] Usando idioma por defecto '{DEFAULT_LANGUAGE}'.")
        with open(f"i18n/{DEFAULT_LANGUAGE}.json", encoding="utf-8") as f:
            _language_data = json.load(f)

def t(key: str, **kwargs) -> str:
    """Traduce una clave y permite interpolación de variables."""
    value = _language_data.get(key, f"[{key}]")
    if kwargs:
        try:
            return value.format(**kwargs)
        except Exception:
            return value
    return value
