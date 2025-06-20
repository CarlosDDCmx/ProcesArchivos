import os
import gettext

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "..", "locale")
DOMAIN = "messages"
TEST_STRINGS = {
    "menu_prin": {
        "es": "🏠 Menú Principal",
        "en": "🏠 Main Menu",
    },
    "herramientas": {
        "es": "🛠 Herramientas",
        "en": "🛠 Tools",
    }
}

def test_language(lang_code: str):
    print(f"\n--- Testing language: {lang_code} ---")
    try:
        translation = gettext.translation(
        DOMAIN,
        localedir=LOCALES_DIR,
        languages=[lang_code],
        fallback=True
    )
    except FileNotFoundError:
        print(f"⚠️  No translation file found for '{lang_code}'")
        return

    _ = translation.gettext

    all_passed = True
    for original, translations in TEST_STRINGS.items():
        expected = translations.get(lang_code, original)
        result = _(original)
        if result == original:
            print(f"⚠️  '{original}' not translated (fallback used?)")
        if result != expected:
            all_passed = False
            print(f"❌ Mismatch for '{original}': got '{result}', expected '{expected}'")
        else:
            print(f"✅ '{original}' -> '{result}'")

    if all_passed:
        print(f"🎉 All translations passed for {lang_code}!\n")
    else:
        print(f"❌ Some translations failed for {lang_code}.\n")

if __name__ == "__main__":
    test_language("es")
    test_language("en")
