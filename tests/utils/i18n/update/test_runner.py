from utils.i18n.update import runner

def test_main_runs(monkeypatch):
    # Simula cada función sin efectos colaterales
    monkeypatch.setattr(runner, "extract_translations", lambda: None)
    monkeypatch.setattr(runner, "init_po_file", lambda: None)
    monkeypatch.setattr(runner, "backup_po_file", lambda: None)
    monkeypatch.setattr(runner, "deduplicate_po", lambda: None)
    monkeypatch.setattr(runner, "merge_translations", lambda: None)
    monkeypatch.setattr(runner, "verify_po", lambda: None)
    monkeypatch.setattr(runner, "compile_mo", lambda: None)

    # Solo prueba que `main()` no lanza errores
    runner.main()
