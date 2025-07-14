from utils.i18n.update import paths

def test_paths_exist():
    assert paths.BASE_DIR.exists()
    assert paths.LOCALE_DIR.name == "locale"
    assert paths.PO_FILE.suffix == ".po"