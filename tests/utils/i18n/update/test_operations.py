from utils.i18n.update import operations
from pathlib import Path

def test_show_duplicates_detects(monkeypatch, tmp_path):
    po = tmp_path / "messages.po"
    po.write_text('msgid "Hello"\nmsgstr ""\nmsgid "Hello"\nmsgstr ""', encoding="utf-8")
    monkeypatch.setattr("builtins.print", lambda *a, **k: None)
    assert operations.show_duplicates(po) is True

def test_show_duplicates_none(monkeypatch, tmp_path):
    po = tmp_path / "messages.po"
    po.write_text('msgid "Hello"\nmsgstr ""\nmsgid "World"\nmsgstr ""', encoding="utf-8")
    monkeypatch.setattr("builtins.print", lambda *a, **k: None)
    assert operations.show_duplicates(po) is False
