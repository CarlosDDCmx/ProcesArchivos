import subprocess
from utils.i18n.update.commands import run

def test_run_success(monkeypatch):
    class DummyCompleted:
        returncode = 0
        stderr = ""
        stdout = "OK"
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: DummyCompleted())
    result = run(["echo", "Hello"])
    assert result.returncode == 0

def test_run_failure(monkeypatch, capsys):
    class DummyFailed:
        returncode = 1
        stderr = "Error simulated"
        stdout = ""
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: DummyFailed())
    result = run(["fail", "command"])
    captured = capsys.readouterr()
    assert "Error al ejecutar" in captured.out
