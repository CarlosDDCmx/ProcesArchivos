import os
from core.i18n import load_language, t

def test_load_and_translate():
    load_language("es")
    assert t("file_not_found", file="a.txt") == "El archivo 'a.txt' no existe."

    load_language("en")
    assert "does not exist" in t("file_not_found", file="a.txt")
