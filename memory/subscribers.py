import json
import logging
from dataclasses import asdict
from pathlib import Path
from memory.bus import MemoryBus
from memory.events import FileAnalyzed, ErrorEvent
from memory import add_event
from utils.i18n.safe import safe_gettext as _

# ── Callback: almacenar el evento ────────────────────────────────────────
def _store_event(evt: FileAnalyzed) -> None:
    add_event(evt)  # actualiza registro y archivo activo

# ── Callback: persistir a disco ──────────────────────────────────────────
_OUT = Path("results")
_OUT.mkdir(exist_ok=True)

def _persist_to_json(evt: FileAnalyzed) -> None:
    data = asdict(evt)
    data["path"] = str(data["path"])
    data["family"] = data["family"].name
    dest = _OUT / f"{evt.path.name}.json"
    dest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ── Callback: log de errores ─────────────────────────────────────────────
def _log_error(evt: ErrorEvent) -> None:
    logging.error("[%s] %s", evt.origin, evt.message)

# ── Registro de callbacks ────────────────────────────────────────────────
MemoryBus.subscribe(FileAnalyzed, _store_event)
MemoryBus.subscribe(FileAnalyzed, _persist_to_json)
MemoryBus.subscribe(ErrorEvent,   _log_error)
